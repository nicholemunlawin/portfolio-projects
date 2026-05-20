# Realtime Clock Date Project

A simple desktop clock app built with Python and Tkinter. It shows the current time, day, and date in a clean window and updates the clock every second.

## Overview

This project is a lightweight GUI application for displaying:

- The current time in `HH:MM:SS AM/PM` format
- The current weekday
- The current date in `Mon DD, YYYY` format

The interface is created with Tkinter, which is included with standard Python installations, so there are no extra runtime dependencies to install.

## Features

- Real-time digital clock that refreshes every second
- Displays the current day and full date
- Custom window title and title bar icon
- Beginner-friendly code structure

## Project Structure

```text
realtime-clock-date-project/
|-- main.py
|-- README.md
|-- pyproject.toml
|-- title-bar-logo.png
|-- uv.lock
```

## Requirements

- Python `3.13` or newer
- Tkinter support enabled in your Python installation

## How It Works

The app uses:

- `Tk()` to create the main window
- `Label` widgets to show the time, day, and date
- `time.strftime()` to get the current system time and date
- `after(1000, ...)` to refresh the displayed time every second

## Run the Project

### Option 1: Run with Python

```bash
python main.py
```

### Option 2: Run with `uv`

```bash
uv run main.py
```

## Output

When launched, the application opens a small desktop window titled `Realtime Date and Time` and displays:

- A large digital clock
- The current weekday
- The current date

## Notes

- The displayed time and date come from your computer's local system settings.
- The file `title-bar-logo.png` is used as the window icon.
- This project is a good starter example for learning Tkinter basics such as labels, layout, and timed UI updates.

## Authoring Context

This is a small educational Python GUI project focused on practicing real-time updates in a desktop interface.
