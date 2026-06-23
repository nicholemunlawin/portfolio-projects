# Number Guessing Game

A command-line number guessing game built with Bash and PostgreSQL. Part of the freeCodeCamp Relational Database certification.

## How It Works

The game picks a random number between 1 and 1000. You get unlimited guesses, and after each one it tells you if the answer is higher or lower. It also tracks your game history using a PostgreSQL database — so it remembers your total games played and your best score (fewest guesses).

## Setup

You'll need:
- Bash
- PostgreSQL

1. Run the SQL dump to create the database and set up the table:

```bash
psql -U freecodecamp < number_guess.sql
```

2. Make the script executable (if it isn't already):

```bash
chmod +x number_guess.sh
```

3. Run the game:

```bash
./number_guess.sh
```

## What the Script Does

- Asks for your username
- If you're new, it creates a profile for you
- If you've played before, it shows your stats (games played + best score)
- Generates a random number between 1 and 1000
- Validates that your input is actually a number
- Keeps track of how many guesses you took
- Updates your stats in the database when you win

## Database

The `users` table stores:
- `username` (unique)
- `user_id` (auto-incremented primary key)
- `games_played` (defaults to 0)
- `best_game` (fewest guesses in a single game, starts as NULL)

## Notes

The `number_guess.sql` file is a PostgreSQL dump that includes the table schema and some test data from when I was building it. You can use it to recreate the database from scratch.
