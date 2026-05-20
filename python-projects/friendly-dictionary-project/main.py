from __future__ import annotations

import json
import threading
import tkinter as tk
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
from urllib import error, parse, request


API_URL_TEMPLATE = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
APP_TITLE = "Friendly Dictionary"
REQUEST_TIMEOUT_SECONDS = 15
MAX_HISTORY_ITEMS = 20
LOGO_FILENAME = "dictionary.png"
HEADER_LOGO_MAX_SIZE = 72


class DictionaryError(Exception):
    """Base exception for dictionary operations."""


class WordNotFoundError(DictionaryError):
    """Raised when the requested word does not exist in the API."""


class DictionaryApiError(DictionaryError):
    """Raised when the API request fails for non-404 reasons."""


@dataclass(slots=True)
class Definition:
    definition: str
    example: str | None
    synonyms: list[str]
    antonyms: list[str]


@dataclass(slots=True)
class Meaning:
    part_of_speech: str
    definitions: list[Definition]
    synonyms: list[str]
    antonyms: list[str]


@dataclass(slots=True)
class DictionaryEntry:
    word: str
    phonetics: list[str]
    audio_urls: list[str]
    meanings: list[Meaning]
    source_urls: list[str]


class HistoryStore:
    """Persist recent searches to a local JSON file."""

    def __init__(self, file_path: Path, max_items: int = MAX_HISTORY_ITEMS) -> None:
        self.file_path = file_path
        self.max_items = max_items

    def load(self) -> list[str]:
        if not self.file_path.exists():
            return []

        try:
            payload = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self._backup_corrupted_file()
            return []

        if not isinstance(payload, dict):
            return []

        history = payload.get("history", [])
        if not isinstance(history, list):
            return []

        sanitized: list[str] = []
        seen: set[str] = set()
        for item in history:
            if isinstance(item, str):
                word = item.strip()
                key = word.casefold()
                if word and key not in seen:
                    sanitized.append(word)
                    seen.add(key)

        return sanitized[: self.max_items]

    def add(self, word: str) -> list[str]:
        history = self.load()
        normalized = word.strip()
        if not normalized:
            return history

        updated = [normalized, *[item for item in history if item.casefold() != normalized.casefold()]]
        updated = updated[: self.max_items]
        self._save(updated)
        return updated

    def clear(self) -> None:
        self._save([])

    def _save(self, history: list[str]) -> None:
        payload = {
            "history": history,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=True),
                encoding="utf-8",
            )
        except OSError as exc:
            raise DictionaryError(f"Unable to save search history: {exc}") from exc

    def _backup_corrupted_file(self) -> None:
        try:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_path = self.file_path.with_suffix(f".corrupt-{timestamp}.json")
            self.file_path.replace(backup_path)
        except OSError:
            # If backup fails we still let the app continue with a clean history.
            return


class DictionaryClient:
    """Client for fetching dictionary entries from the free API."""

    def fetch(self, word: str) -> DictionaryEntry:
        clean_word = word.strip()
        if not clean_word:
            raise DictionaryError("Please enter a word to search.")

        encoded_word = parse.quote(clean_word)
        url = API_URL_TEMPLATE.format(word=encoded_word)
        req = request.Request(
            url,
            headers={
                "User-Agent": "FriendlyDictionaryApp/1.0 (+https://dictionaryapi.dev)"
            },
        )

        try:
            with request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            if exc.code == 404:
                raise WordNotFoundError(f'No dictionary entry was found for "{clean_word}".') from exc
            raise DictionaryApiError(f"Dictionary API returned HTTP {exc.code}.") from exc
        except error.URLError as exc:
            raise DictionaryApiError(
                "Unable to reach the dictionary service. Check your internet connection and try again."
            ) from exc
        except json.JSONDecodeError as exc:
            raise DictionaryApiError("The dictionary service returned an unreadable response.") from exc

        if not isinstance(data, list) or not data:
            raise DictionaryApiError("The dictionary service returned an unexpected response.")

        return self._parse_entry(data[0])

    def _parse_entry(self, payload: dict) -> DictionaryEntry:
        word = str(payload.get("word", "")).strip() or "Unknown"
        phonetics = [
            str(item.get("text", "")).strip()
            for item in payload.get("phonetics", [])
            if isinstance(item, dict) and str(item.get("text", "")).strip()
        ]
        audio_urls = [
            str(item.get("audio", "")).strip()
            for item in payload.get("phonetics", [])
            if isinstance(item, dict) and str(item.get("audio", "")).strip()
        ]

        meanings: list[Meaning] = []
        for meaning_payload in payload.get("meanings", []):
            if not isinstance(meaning_payload, dict):
                continue

            definition_items: list[Definition] = []
            for definition_payload in meaning_payload.get("definitions", []):
                if not isinstance(definition_payload, dict):
                    continue

                definition_text = str(definition_payload.get("definition", "")).strip()
                if not definition_text:
                    continue

                definition_items.append(
                    Definition(
                        definition=definition_text,
                        example=self._optional_text(definition_payload.get("example")),
                        synonyms=self._deduplicate_strings(definition_payload.get("synonyms", [])),
                        antonyms=self._deduplicate_strings(definition_payload.get("antonyms", [])),
                    )
                )

            if definition_items:
                meanings.append(
                    Meaning(
                        part_of_speech=str(meaning_payload.get("partOfSpeech", "General")).strip() or "General",
                        definitions=definition_items,
                        synonyms=self._deduplicate_strings(meaning_payload.get("synonyms", [])),
                        antonyms=self._deduplicate_strings(meaning_payload.get("antonyms", [])),
                    )
                )

        return DictionaryEntry(
            word=word,
            phonetics=self._deduplicate_strings(phonetics),
            audio_urls=self._deduplicate_strings(audio_urls),
            meanings=meanings,
            source_urls=self._deduplicate_strings(payload.get("sourceUrls", [])),
        )

    @staticmethod
    def _optional_text(value: object) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _deduplicate_strings(values: object) -> list[str]:
        if not isinstance(values, list):
            return []

        unique_values: list[str] = []
        seen: set[str] = set()
        for item in values:
            if not isinstance(item, str):
                continue
            text = item.strip()
            key = text.casefold()
            if text and key not in seen:
                unique_values.append(text)
                seen.add(key)
        return unique_values


class DictionaryApp(tk.Tk):
    """Tkinter GUI for searching dictionary definitions."""

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x720")
        self.minsize(900, 620)
        self.configure(bg="#f4f7fb")

        project_root = Path(__file__).resolve().parent
        self.logo_path = project_root / LOGO_FILENAME
        self.history_store = HistoryStore(project_root / "data" / "search_history.json")
        self.client = DictionaryClient()
        self.history = self.history_store.load()
        self.current_entry: DictionaryEntry | None = None
        self.app_logo_image: tk.PhotoImage | None = None
        self.header_logo_image: tk.PhotoImage | None = None

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Search for any English word to see its definition, examples, and related terms.")

        self._load_logo_assets()
        self._configure_theme()
        self._build_layout()
        self._populate_history()

    def _load_logo_assets(self) -> None:
        if not self.logo_path.exists():
            self.status_var.set(f'Logo file "{LOGO_FILENAME}" was not found. Running without a logo.')
            return

        try:
            self.app_logo_image = tk.PhotoImage(file=str(self.logo_path))
        except tk.TclError:
            self.status_var.set(f'Logo file "{LOGO_FILENAME}" could not be opened. Running without a logo.')
            return

        self.header_logo_image = self._create_header_logo(self.app_logo_image)

        try:
            self.iconphoto(True, self.app_logo_image)
        except tk.TclError:
            # Some Tk builds do not support window icons in the current environment.
            pass

    @staticmethod
    def _create_header_logo(image: tk.PhotoImage) -> tk.PhotoImage:
        width = max(image.width(), 1)
        height = max(image.height(), 1)
        scale = max(width / HEADER_LOGO_MAX_SIZE, height / HEADER_LOGO_MAX_SIZE, 1)
        subsample_factor = max(int(scale), 1)
        return image.subsample(subsample_factor, subsample_factor)

    def _configure_theme(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#f4f7fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#ffffff", foreground="#17324d", font=("Segoe UI Semibold", 16))
        style.configure("Subtitle.TLabel", background="#ffffff", foreground="#59708a", font=("Segoe UI", 10))
        style.configure("Status.TLabel", background="#f4f7fb", foreground="#34506d", font=("Segoe UI", 10))
        style.configure("Primary.TButton", font=("Segoe UI Semibold", 10))

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=18, style="App.TFrame")
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)

        header = ttk.Frame(container, padding=(18, 18, 18, 12), style="Card.TFrame")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 12))
        header.columnconfigure(1, weight=1)

        if self.header_logo_image is not None:
            logo_label = ttk.Label(header, image=self.header_logo_image, style="Card.TFrame")
            logo_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 14))

        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(
            header,
            text="A simple desktop dictionary powered by a free public API.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=1, sticky="w", pady=(4, 0))

        search_bar = ttk.Frame(header, style="Card.TFrame")
        search_bar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        search_bar.columnconfigure(0, weight=1)

        self.search_entry = ttk.Entry(search_bar, textvariable=self.search_var, font=("Segoe UI", 12))
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<Return>", self._on_submit)

        self.search_button = ttk.Button(
            search_bar,
            text="Search",
            style="Primary.TButton",
            command=self.start_search,
        )
        self.search_button.grid(row=0, column=1, sticky="ew")

        sidebar = ttk.Frame(container, padding=16, style="Card.TFrame")
        sidebar.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(1, weight=1)

        ttk.Label(sidebar, text="Recent Searches", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.history_listbox = tk.Listbox(
            sidebar,
            activestyle="none",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 11),
            selectbackground="#dcecff",
            selectforeground="#17324d",
        )
        self.history_listbox.grid(row=1, column=0, sticky="nsew", pady=(12, 12))
        self.history_listbox.bind("<Double-Button-1>", self._on_history_selected)

        sidebar_actions = ttk.Frame(sidebar, style="Card.TFrame")
        sidebar_actions.grid(row=2, column=0, sticky="ew")
        sidebar_actions.columnconfigure(0, weight=1)
        sidebar_actions.columnconfigure(1, weight=1)

        ttk.Button(sidebar_actions, text="Use Selected", command=self._search_selected_history).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(sidebar_actions, text="Clear History", command=self._clear_history).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

        content = ttk.Frame(container, padding=16, style="Card.TFrame")
        content.grid(row=1, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        self.word_label = ttk.Label(content, text="Word details will appear here", style="Title.TLabel")
        self.word_label.grid(row=0, column=0, sticky="w")

        self.result_text = tk.Text(
            content,
            wrap="word",
            font=("Segoe UI", 11),
            padx=14,
            pady=14,
            relief="flat",
            bg="#fbfdff",
            fg="#1b2c3e",
            state="disabled",
        )
        self.result_text.grid(row=1, column=0, sticky="nsew", pady=(12, 12))

        result_actions = ttk.Frame(content, style="Card.TFrame")
        result_actions.grid(row=2, column=0, sticky="ew")
        result_actions.columnconfigure(0, weight=0)
        result_actions.columnconfigure(1, weight=0)
        result_actions.columnconfigure(2, weight=1)

        self.source_button = ttk.Button(
            result_actions,
            text="Open Source",
            command=self._open_source_url,
            state="disabled",
        )
        self.source_button.grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.audio_button = ttk.Button(
            result_actions,
            text="Open Pronunciation Audio",
            command=self._open_audio_url,
            state="disabled",
        )
        self.audio_button.grid(row=0, column=1, sticky="w")

        status_label = ttk.Label(container, textvariable=self.status_var, style="Status.TLabel")
        status_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        self.search_entry.focus_set()

    def _populate_history(self) -> None:
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def _set_results_text(self, content: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, content)
        self.result_text.configure(state="disabled")
        self.result_text.see("1.0")

    def _on_submit(self, _event: tk.Event) -> None:
        self.start_search()

    def _on_history_selected(self, _event: tk.Event) -> None:
        self._search_selected_history()

    def _search_selected_history(self) -> None:
        selection = self.history_listbox.curselection()
        if not selection:
            self.status_var.set("Select a recent word first.")
            return

        self.search_var.set(self.history_listbox.get(selection[0]))
        self.start_search()

    def _clear_history(self) -> None:
        if not self.history:
            self.status_var.set("Search history is already empty.")
            return

        confirm = messagebox.askyesno(APP_TITLE, "Clear all saved search history?")
        if not confirm:
            return

        try:
            self.history_store.clear()
        except DictionaryError as exc:
            messagebox.showerror(APP_TITLE, str(exc))
            return

        self.history = []
        self._populate_history()
        self.status_var.set("Search history cleared.")

    def start_search(self) -> None:
        word = self.search_var.get().strip()
        if not word:
            messagebox.showwarning(APP_TITLE, "Enter a word before searching.")
            return

        self.search_button.configure(state="disabled")
        self.status_var.set(f'Searching for "{word}"...')
        self._set_results_text("Loading dictionary results...")
        self.word_label.configure(text="Searching...")
        self.source_button.configure(state="disabled")
        self.audio_button.configure(state="disabled")

        worker = threading.Thread(target=self._search_in_background, args=(word,), daemon=True)
        worker.start()

    def _search_in_background(self, word: str) -> None:
        try:
            entry = self.client.fetch(word)
        except DictionaryError as exc:
            self.after(0, lambda: self._handle_search_error(str(exc)))
            return
        except Exception:
            self.after(
                0,
                lambda: self._handle_search_error(
                    "Something unexpected happened while searching. Please try again."
                ),
            )
            return

        self.after(0, lambda: self._handle_search_success(entry))

    def _handle_search_error(self, message: str) -> None:
        self.current_entry = None
        self.search_button.configure(state="normal")
        self.word_label.configure(text="No result")
        self._set_results_text(message)
        self.status_var.set(message)

    def _handle_search_success(self, entry: DictionaryEntry) -> None:
        self.current_entry = entry
        self.search_button.configure(state="normal")
        self.word_label.configure(text=entry.word.title())
        self._set_results_text(self._format_entry(entry))
        self.status_var.set(f'Displaying results for "{entry.word}".')
        self.source_button.configure(state="normal" if entry.source_urls else "disabled")
        self.audio_button.configure(state="normal" if entry.audio_urls else "disabled")

        try:
            self.history = self.history_store.add(entry.word)
        except DictionaryError as exc:
            self.status_var.set(f'Displaying results for "{entry.word}", but history could not be saved: {exc}')
        self._populate_history()

    def _format_entry(self, entry: DictionaryEntry) -> str:
        lines: list[str] = [f"Word: {entry.word}"]

        if entry.phonetics:
            lines.append(f"Pronunciation: {' | '.join(entry.phonetics)}")

        if entry.source_urls:
            lines.append(f"Source: {entry.source_urls[0]}")

        for meaning in entry.meanings:
            lines.append("")
            lines.append(f"[{meaning.part_of_speech}]")

            if meaning.synonyms:
                lines.append(f"Synonyms: {', '.join(meaning.synonyms[:8])}")
            if meaning.antonyms:
                lines.append(f"Antonyms: {', '.join(meaning.antonyms[:8])}")

            for index, definition in enumerate(meaning.definitions, start=1):
                lines.append(f"{index}. {definition.definition}")
                if definition.example:
                    lines.append(f"   Example: {definition.example}")
                if definition.synonyms:
                    lines.append(f"   Definition synonyms: {', '.join(definition.synonyms[:8])}")
                if definition.antonyms:
                    lines.append(f"   Definition antonyms: {', '.join(definition.antonyms[:8])}")

        if not entry.meanings:
            lines.append("")
            lines.append("No meanings were available in the API response.")

        return "\n".join(lines)

    def _open_source_url(self) -> None:
        if self.current_entry and self.current_entry.source_urls:
            webbrowser.open(self.current_entry.source_urls[0])

    def _open_audio_url(self) -> None:
        if self.current_entry and self.current_entry.audio_urls:
            webbrowser.open(self.current_entry.audio_urls[0])


def main() -> None:
    app = DictionaryApp()
    app.mainloop()


if __name__ == "__main__":
    main()
