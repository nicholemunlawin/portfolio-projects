# Personal Expense Tracker

A simple command-line Python app for recording daily expenses, viewing saved entries, and checking total spending.

## Features

- Add an expense with category, amount, and description
- Save expenses to a local `expenses.csv` file
- View all recorded expenses in a table-like format
- Calculate the total amount spent

## Tech Stack

- Python 3.13+
- Standard library only (`csv`, `os`, `datetime`)

## Project Structure

```text
personal-expense-tracker-project/
|- main.py
|- expenses.csv
|- pyproject.toml
|- README.md
```

## Getting Started

### 1. Clone the project

```bash
git clone <your-repository-url>
cd personal-expense-tracker-project
```

### 2. Run the application

Using Python:

```bash
python main.py
```

Or, if you use `uv`:

```bash
uv run main.py
```

## How It Works

When you run the program, you'll see this menu:

```text
--- Personal Expense Tracker ---
1. Add Expense
2. View All Expenses
3. View Total Spending
4. Exit
```

### Add Expense

Lets you enter:

- Category
- Amount
- Short description

Each record is saved with the current date and time.

### View All Expenses

Displays every saved expense from `expenses.csv`.

### View Total Spending

Adds all saved amounts and shows the total spending.

## Data Storage

- Expenses are stored in `expenses.csv`
- The CSV file is created automatically if it does not exist
- CSV files are currently ignored by Git through `.gitignore`

## Example CSV Format

```csv
Date,Category,Amount,Description
2026-04-10 12:27:18,Food,560.00,Burger King
2026-04-10 12:27:38,Transport,1000.00,Gas
```

## Possible Improvements

- Edit or delete existing expenses
- Filter expenses by category or date
- Add monthly summaries and reports
- Export reports in other formats

## License

This project is open for personal and educational use.
