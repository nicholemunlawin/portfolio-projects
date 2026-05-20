# URL Shortener Project

A simple beginner-friendly Python 3 command-line URL shortener.

This project lets users enter a long URL and get back a shorter version such as `short.ly/abc123`. It stores URL mappings in a Python dictionary while the program is running, so it is great for practicing core Python concepts like dictionaries, functions, loops, conditionals, and input handling.

## Features

- Shorten a long URL into a random 6-character short code
- Expand a short URL back into the original URL
- View all saved URLs in the current session
- Reject blank input
- Show a helpful error if a short code is not found
- Keep everything in one Python file
- Use no database and no external libraries

## How It Works

The program uses:

- A Python dictionary to store short codes and original URLs
- Randomly generated 6-character codes made from:
  - Uppercase letters
  - Lowercase letters
  - Digits
- A check to make sure each generated short code is unique

Example dictionary:

```python
{
    "Ab12Cd": "https://www.example.com/very/long/url"
}
```

## Project Files

- [main.py](F:\Python Projects\url-shortener-project\main.py:1) - the full URL shortener application
- [README.md](F:\Python Projects\url-shortener-project\README.md:1) - project documentation

## Requirements

- Python 3

No extra packages are needed.

## How to Run

From the project folder, run:

```bash
python main.py
```

## Menu Options

When the program starts, you will see:

```text
1. Shorten URL
2. Expand short URL
3. View all saved URLs
4. Quit
```

## Sample Run

```text
Welcome to the Python URL Shortener!

URL Shortener Menu
1. Shorten URL
2. Expand short URL
3. View all saved URLs
4. Quit
Choose an option (1-4): 1
Enter the long URL: https://www.example.com/my/very/long/link
Short URL created: short.ly/aB3xY9

URL Shortener Menu
1. Shorten URL
2. Expand short URL
3. View all saved URLs
4. Quit
Choose an option (1-4): 2
Enter the short URL or short code: short.ly/aB3xY9
Original URL: https://www.example.com/my/very/long/link

URL Shortener Menu
1. Shorten URL
2. Expand short URL
3. View all saved URLs
4. Quit
Choose an option (1-4): 3

Saved URLs:
short.ly/aB3xY9 -> https://www.example.com/my/very/long/link

URL Shortener Menu
1. Shorten URL
2. Expand short URL
3. View all saved URLs
4. Quit
Choose an option (1-4): 4
Goodbye!
```

## Notes

- URL data is only stored in memory while the program is running
- Once the program closes, saved URLs are lost
- This project is meant for learning and practice, not production use
