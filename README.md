# Friendly Dictionary App

A user-friendly desktop dictionary application built with Python and Tkinter. It uses the free [Dictionary API](https://dictionaryapi.dev/) to fetch word meanings, pronunciations, synonyms, antonyms, and examples.

## Features

- Clean desktop GUI built with the Python standard library
- Word lookup using a free public dictionary API
- Displays phonetics, parts of speech, meanings, examples, synonyms, and antonyms
- Recent search history saved locally to `data/search_history.json`
- Safe file handling for missing or corrupted history files
- Error handling for empty input, missing words, API failures, and offline/network issues
- No third-party dependencies required

## Project Structure

```text
dictionary-app-project/
|-- .gitignore
|-- .python-version
|-- main.py
|-- pyproject.toml
|-- README.md
```

The `data/` folder is created automatically when the app saves search history for the first time.

## Requirements

- Python 3.13 or newer
- Internet connection for dictionary searches

## Run The App

```bash
python main.py
```

## API Used

- Free Dictionary API: [https://dictionaryapi.dev/](https://dictionaryapi.dev/)
- Current request format used by this app: `https://api.dictionaryapi.dev/api/v2/entries/en/<word>`

## Notes

- Search history is stored locally and can be cleared from the GUI.
- If the history file becomes invalid, the app backs it up and starts with a clean history file.
- Pronunciation audio and source links can be opened from the app when available in the API response.
