# PCSO Lotto Generator

Small Python app for generating a PCSO lotto combination that has not appeared in the scraped history for the selected game.

The GUI is built with Tkinter. Historical data is stored in `pcso_lotto_results.csv`. Each time `main.py` starts, it checks the latest saved draw date and updates from that date through today.

## Features

- Automatically creates `pcso_lotto_results.csv` on first run.
- Updates the CSV on every launch without re-downloading the full history.
- Lets the user choose a lotto game from a dropdown.
- Groups games in the dropdown by value count, such as `2 values`, `3 digits`, and `6 numbers`.
- Generates combinations that are not already present in the selected game's history.
- Uses distinct sorted numbers for classic 6-number games like `Grand Lotto 6/55`.
- Allows repeated values for digit-style games like `3D Lotto`, `4D Lotto`, and `6D Lotto`.
- Excludes `6D Lotto` from the historical uniqueness rule.

## Requirements

- Python 3.13+
- Google Chrome, for the Selenium scraper
- Project dependencies from `pyproject.toml`

## Setup

If you are using `uv`:

```powershell
uv sync
```

Or install the dependencies into your active environment:

```powershell
pip install pandas selenium lxml requests
```

## Run The App

Run:

```powershell
.\.venv\Scripts\python.exe .\main.py
```

On startup, the app checks `pcso_lotto_results.csv` before opening the generator.

If the CSV is missing, the app scrapes the full history from 2016 through today. This first run can take a few minutes.

If the CSV already exists, the app reads the latest `draw_date` and scrapes only from that date through today. Existing rows are de-duplicated when the update is saved.

After the GUI opens, choose a game, click `Generate`, then optionally click `Copy`.

Note: the PCSO site may occasionally block automated access. If that happens, try again later or use a different network.

## How Uniqueness Is Checked

For 6-number lotto games, combinations are sorted before checking history because order does not matter.

For digit-style games, the drawn order is preserved because `1-2-3` and `3-2-1` are different results.

`6D Lotto` is generated as a digit-style game, but it is not checked against historical results for uniqueness.

This app only checks whether a generated combination already exists in the scraped historical data. It does not predict future winning numbers.
