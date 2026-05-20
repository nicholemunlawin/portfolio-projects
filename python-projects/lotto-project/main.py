"""Tkinter app for generating PCSO combinations not found in scraped history."""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from itertools import product
from math import comb
from pathlib import Path
from queue import Empty, Queue
from random import randint, sample
import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
# Maintained by lotto-results.py. Keeping it relative makes the app portable.
HISTORY_CSV = BASE_DIR / "pcso_lotto_results.csv"
SCRAPER_SCRIPT = BASE_DIR / "lotto-results.py"


@dataclass(frozen=True)
class GameRule:
    count: int
    minimum: int
    maximum: int
    distinct_numbers: bool
    order_matters: bool
    display_width: int


# Classic lotto games: order does not matter, and numbers should not repeat.
SIX_NUMBER_RULES = {
    "Grand Lotto 6/55": GameRule(6, 1, 55, True, False, 2),
    "Lotto 6/42": GameRule(6, 1, 42, True, False, 2),
    "Megalotto 6/45": GameRule(6, 1, 45, True, False, 2),
    "Superlotto 6/49": GameRule(6, 1, 49, True, False, 2),
    "Ultra Lotto 6/58": GameRule(6, 1, 58, True, False, 2),
}


# Digit-style games keep draw order. Some of them can contain repeated values.
DIGIT_GAME_RULES = {
    "2D Lotto 2PM": GameRule(2, 1, 31, False, True, 2),
    "2D Lotto 5PM": GameRule(2, 1, 31, False, True, 2),
    "2D Lotto 9PM": GameRule(2, 1, 31, False, True, 2),
    "EZ2 Lotto 11:30AM": GameRule(2, 1, 31, False, True, 2),
    "EZ2 Lotto 12:30PM": GameRule(2, 1, 31, False, True, 2),
    "EZ2 Lotto 2PM": GameRule(2, 1, 31, False, True, 2),
    "3D Lotto 2PM": GameRule(3, 0, 9, False, True, 1),
    "3D Lotto 5PM": GameRule(3, 0, 9, False, True, 1),
    "3D Lotto 9PM": GameRule(3, 0, 9, False, True, 1),
    "Suertres Lotto 11:30AM": GameRule(3, 0, 9, False, True, 1),
    "Suertres Lotto 12:30PM": GameRule(3, 0, 9, False, True, 1),
    "Suertres Lotto 2PM": GameRule(3, 0, 9, False, True, 1),
    "4D Lotto": GameRule(4, 0, 9, False, True, 1),
    "6D Lotto": GameRule(6, 0, 9, False, True, 1),
}


GAME_RULES = SIX_NUMBER_RULES | DIGIT_GAME_RULES
GAMES_WITHOUT_HISTORY_UNIQUENESS = {"6D Lotto"}


def get_rule(game_name: str) -> GameRule | None:
    if game_name in GAME_RULES:
        return GAME_RULES[game_name]

    match = re.search(r"\b6/(\d+)\b", game_name)
    if match:
        return GameRule(6, 1, int(match.group(1)), True, False, 2)

    return None


def uses_history_uniqueness(game_name: str) -> bool:
    return game_name not in GAMES_WITHOUT_HISTORY_UNIQUENESS


def update_history_csv(csv_path: Path = HISTORY_CSV) -> None:
    if not SCRAPER_SCRIPT.exists():
        raise FileNotFoundError(f"Scraper script was not found: {SCRAPER_SCRIPT}")

    spec = importlib.util.spec_from_file_location("lotto_results", SCRAPER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load scraper script: {SCRAPER_SCRIPT}")

    scraper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scraper)

    # lotto-results.py has a hyphen in its filename, so load it by path.
    scraper.update_history_csv(str(csv_path))

    if not csv_path.exists():
        raise RuntimeError(f"The scraper finished, but {csv_path.name} was not created.")


def load_history(csv_path: Path = HISTORY_CSV, auto_scrape: bool = True) -> pd.DataFrame:
    if auto_scrape:
        update_history_csv(csv_path)
    elif not csv_path.exists():
        raise FileNotFoundError(f"Historical data was not found: {csv_path}.")

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Historical data was not found: {csv_path}. "
            "The automatic scrape did not create pcso_lotto_results.csv."
        )

    df = pd.read_csv(csv_path)
    required_columns = {"lotto_game", "combinations"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"{csv_path.name} is missing required column(s): {missing}")

    return df


def parse_combination(value: object) -> tuple[int, ...] | None:
    if pd.isna(value):
        return None

    parts = [part.strip() for part in str(value).split("-") if part.strip()]

    try:
        return tuple(int(part) for part in parts)
    except ValueError:
        return None


def normalize_combination(
    numbers: tuple[int, ...], rule: GameRule
) -> tuple[int, ...] | None:
    """Return the lookup-safe form of a combination, or None if invalid."""
    if len(numbers) != rule.count:
        return None

    if any(number < rule.minimum or number > rule.maximum for number in numbers):
        return None

    if rule.distinct_numbers and len(set(numbers)) != len(numbers):
        return None

    if rule.order_matters:
        return numbers

    return tuple(sorted(numbers))


def build_history_index(df: pd.DataFrame) -> dict[str, set[tuple[int, ...]]]:
    # Sets make "is this already drawn?" checks fast even with thousands of rows.
    history: dict[str, set[tuple[int, ...]]] = {}

    for game_name, game_rows in df.groupby("lotto_game"):
        game_name = str(game_name)
        rule = get_rule(game_name)
        if rule is None:
            continue

        used_combinations: set[tuple[int, ...]] = set()

        if not uses_history_uniqueness(game_name):
            history[game_name] = used_combinations
            continue

        for value in game_rows["combinations"]:
            numbers = parse_combination(value)
            if numbers is None:
                continue

            normalized = normalize_combination(numbers, rule)
            if normalized is not None:
                used_combinations.add(normalized)

        if used_combinations:
            history[game_name] = used_combinations

    return history


def total_possible_combinations(rule: GameRule) -> int:
    value_count = rule.maximum - rule.minimum + 1

    if rule.distinct_numbers:
        return comb(value_count, rule.count)

    return value_count**rule.count


def create_candidate(rule: GameRule) -> tuple[int, ...]:
    if rule.distinct_numbers:
        return tuple(sorted(sample(range(rule.minimum, rule.maximum + 1), rule.count)))

    return tuple(randint(rule.minimum, rule.maximum) for _ in range(rule.count))


def iter_small_search_space(rule: GameRule):
    values = range(rule.minimum, rule.maximum + 1)

    if rule.distinct_numbers:
        return

    yield from product(values, repeat=rule.count)


def format_combination(numbers: tuple[int, ...], rule: GameRule) -> str:
    return "-".join(f"{number:0{rule.display_width}d}" for number in numbers)


def is_in_history(
    game_name: str,
    numbers: tuple[int, ...],
    history: dict[str, set[tuple[int, ...]]],
) -> bool:
    rule = get_rule(game_name)
    if rule is None:
        return False

    if not uses_history_uniqueness(game_name):
        return False

    normalized = normalize_combination(numbers, rule)
    if normalized is None:
        return False

    return normalized in history.get(game_name, set())


def generate_for_game(
    game_name: str, history: dict[str, set[tuple[int, ...]]]
) -> tuple[int, ...]:
    rule = get_rule(game_name)

    if rule is None:
        raise ValueError(f"No generation rule is configured for {game_name}.")

    used_combinations = history.get(game_name, set())
    possible_count = total_possible_combinations(rule)

    if len(used_combinations) >= possible_count:
        raise RuntimeError(
            f"Every possible {game_name} combination is already in the history file."
        )

    max_attempts = min(max(possible_count * 3, 1_000), 100_000)

    for _ in range(max_attempts):
        numbers = create_candidate(rule)
        normalized = normalize_combination(numbers, rule)

        if (
            normalized is not None
            and normalized not in used_combinations
            and not is_in_history(game_name, numbers, history)
        ):
            return numbers

    if possible_count <= 100_000:
        # Small games such as 2D/3D can get crowded, so fall back to a full scan.
        for numbers in iter_small_search_space(rule):
            normalized = normalize_combination(tuple(numbers), rule)

            if (
                normalized is not None
                and normalized not in used_combinations
                and not is_in_history(game_name, tuple(numbers), history)
            ):
                return tuple(numbers)

    raise RuntimeError(f"No unused {game_name} combination was found.")


def game_group_label(game_name: str) -> str:
    rule = get_rule(game_name)

    if rule is None:
        return "Other"

    if rule.count == 6 and rule.distinct_numbers:
        return "6 numbers"

    if rule.maximum == 9:
        return f"{rule.count} digits"

    return f"{rule.count} values"


def game_sort_key(game_name: str) -> tuple[int, int, str]:
    rule = get_rule(game_name)

    if rule is None:
        return (99, 99, game_name)

    group_order = 1 if rule.count == 6 and rule.distinct_numbers else 0
    return (rule.count, group_order, game_name)


def format_game_option(game_name: str) -> str:
    # ttk.Combobox has no real group headers, so each option carries its group.
    return f"{game_group_label(game_name):<9} | {game_name}"


class LottoGeneratorApp:
    def __init__(self, root: tk.Tk, history_df: pd.DataFrame):
        self.root = root
        self.history = build_history_index(history_df)
        self.games = sorted(self.history, key=game_sort_key)
        self.game_options = [format_game_option(game_name) for game_name in self.games]
        self.game_by_option = dict(zip(self.game_options, self.games))

        if not self.games:
            raise ValueError("No supported lotto games were found in the history file.")

        self.selected_game = tk.StringVar(value=self.game_options[0])
        self.result = tk.StringVar(value="--")

        self.configure_window()
        self.icons = self.create_icons()
        self.build_widgets()

    def configure_window(self) -> None:
        self.root.title("PCSO Lotto Generator")
        self.root.minsize(520, 260)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_icons(self) -> dict[str, tk.PhotoImage]:
        # Tiny in-memory icons avoid extra image files beside the script.
        def draw_rect(
            image: tk.PhotoImage,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            color: str,
        ) -> None:
            image.put(color, to=(x1, y1, x2, y2))

        app_icon = tk.PhotoImage(width=28, height=28)
        draw_rect(app_icon, 3, 3, 25, 25, "#1d4ed8")
        draw_rect(app_icon, 6, 6, 22, 22, "#2563eb")
        for x, y in ((8, 8), (14, 14), (20, 20), (20, 8), (8, 20)):
            draw_rect(app_icon, x, y, x + 3, y + 3, "#ffffff")

        generate_icon = tk.PhotoImage(width=18, height=18)
        draw_rect(generate_icon, 3, 3, 15, 15, "#2563eb")
        draw_rect(generate_icon, 5, 5, 13, 13, "#ffffff")
        for x, y in ((5, 5), (11, 5), (8, 8), (5, 11), (11, 11)):
            draw_rect(generate_icon, x, y, x + 2, y + 2, "#2563eb")

        copy_icon = tk.PhotoImage(width=18, height=18)
        draw_rect(copy_icon, 4, 2, 14, 4, "#2563eb")
        draw_rect(copy_icon, 4, 2, 6, 12, "#2563eb")
        draw_rect(copy_icon, 12, 2, 14, 12, "#2563eb")
        draw_rect(copy_icon, 4, 10, 14, 12, "#2563eb")
        draw_rect(copy_icon, 7, 6, 16, 8, "#0f172a")
        draw_rect(copy_icon, 7, 6, 9, 16, "#0f172a")
        draw_rect(copy_icon, 14, 6, 16, 16, "#0f172a")
        draw_rect(copy_icon, 7, 14, 16, 16, "#0f172a")

        return {
            "app": app_icon,
            "generate": generate_icon,
            "copy": copy_icon,
        }

    def build_widgets(self) -> None:
        frame = ttk.Frame(self.root, padding=24)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        header = ttk.Frame(frame)
        header.grid(row=0, column=0, sticky="w")

        ttk.Label(header, image=self.icons["app"]).grid(row=0, column=0, padx=(0, 10))
        title = ttk.Label(
            header,
            text="PCSO Lotto Generator",
            font=("Segoe UI", 18, "bold"),
        )
        title.grid(row=0, column=1)

        ttk.Label(frame, text="Lotto game").grid(row=1, column=0, sticky="w", pady=(24, 4))

        game_picker = ttk.Combobox(
            frame,
            textvariable=self.selected_game,
            values=self.game_options,
            state="readonly",
            height=12,
        )
        game_picker.grid(row=2, column=0, sticky="ew")
        game_picker.bind("<<ComboboxSelected>>", self.clear_result)

        result_label = ttk.Label(
            frame,
            textvariable=self.result,
            font=("Segoe UI", 28, "bold"),
            anchor="center",
        )
        result_label.grid(row=3, column=0, sticky="ew", pady=(28, 22))

        actions = ttk.Frame(frame)
        actions.grid(row=4, column=0, sticky="ew")
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        ttk.Button(
            actions,
            text="Generate",
            image=self.icons["generate"],
            compound="left",
            command=self.generate,
        ).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(
            actions,
            text="Copy",
            image=self.icons["copy"],
            compound="left",
            command=self.copy_result,
        ).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def clear_result(self, event=None) -> None:
        self.result.set("--")

    def generate(self) -> None:
        game_name = self.game_by_option.get(
            self.selected_game.get(),
            self.selected_game.get(),
        )

        try:
            rule = get_rule(game_name)
            numbers = generate_for_game(game_name, self.history)
        except Exception as exc:
            messagebox.showerror("Generation failed", str(exc))
            return

        if rule is None:
            return

        if is_in_history(game_name, numbers, self.history):
            messagebox.showerror(
                "Generation failed",
                "Generated combination already exists in historical data. Try again.",
            )
            return

        formatted = format_combination(numbers, rule)
        self.result.set(formatted)

    def copy_result(self) -> None:
        value = self.result.get()
        if value == "--":
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(value)


def build_startup_screen(root: tk.Tk) -> ttk.Frame:
    root.title("PCSO Lotto Generator")
    root.minsize(520, 220)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=24)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(0, weight=1)

    ttk.Label(
        frame,
        text="Preparing lotto history",
        font=("Segoe UI", 18, "bold"),
    ).grid(row=0, column=0, sticky="w")

    ttk.Label(
        frame,
        text=(
            "The app is checking PCSO historical results and updating from "
            "the latest saved draw date before opening the generator."
        ),
        wraplength=460,
    ).grid(row=1, column=0, sticky="w", pady=(16, 18))

    progress = ttk.Progressbar(frame, mode="indeterminate")
    progress.grid(row=2, column=0, sticky="ew")
    progress.start(12)

    return frame


def open_generator(root: tk.Tk, history_df: pd.DataFrame) -> None:
    for child in root.winfo_children():
        child.destroy()

    LottoGeneratorApp(root, history_df)


def show_startup_error(root: tk.Tk, exc: Exception) -> None:
    root.withdraw()
    messagebox.showerror("PCSO Lotto Generator", str(exc))
    root.destroy()


def main() -> None:
    root = tk.Tk()

    build_startup_screen(root)
    results: Queue[tuple[str, pd.DataFrame | Exception]] = Queue()

    def load_in_background() -> None:
        try:
            results.put(("ok", load_history(auto_scrape=True)))
        except Exception as exc:
            results.put(("error", exc))

    def check_startup_result() -> None:
        try:
            status, payload = results.get_nowait()
        except Empty:
            root.after(250, check_startup_result)
            return

        if status == "ok" and isinstance(payload, pd.DataFrame):
            open_generator(root, payload)
        elif isinstance(payload, Exception):
            show_startup_error(root, payload)

    threading.Thread(target=load_in_background, daemon=True).start()
    root.after(250, check_startup_result)

    root.mainloop()


if __name__ == "__main__":
    main()
