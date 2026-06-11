# Worldcup Database Project

This is a freeCodeCamp Relational Database certification project. It's a PostgreSQL database that stores FIFA World Cup match data from 2014 and 2018, along with some bash scripts to load and query the data.

## What's in here

- `worldcup.sql` -- creates the database, tables, and loads all the data
- `games.csv` -- the raw match data (32 games total)
- `insert_data.sh` -- reads the CSV and populates the database
- `queries.sh` -- runs a bunch of analytical queries against the data
- `expected_output.txt` -- what the queries should output (for the test runner)

## How to use it

You'll need PostgreSQL installed. To set up the database:

```bash
psql -U postgres < worldcup.sql
```

To populate from the CSV instead of the SQL dump:

```bash
./insert_data.sh
```

Run the queries:

```bash
./queries.sh
```

There's also a test mode that uses a separate `worldcuptest` database:

```bash
./insert_data.sh test
```

## Database schema

Two tables -- pretty straightforward:

**teams**
| Column | Type | Notes |
|--------|------|-------|
| team_id | serial | primary key |
| name | varchar(50) | unique |

**games**
| Column | Type | Notes |
|--------|------|-------|
| game_id | serial | primary key |
| year | int | 2014 or 2018 |
| round | varchar(25) | Eighth-Final, Quarter-Final, etc. |
| winner_id | int | foreign key -> teams |
| opponent_id | int | foreign key -> teams |
| winner_goals | int | |
| opponent_goals | int | |

The `ON CONFLICT DO NOTHING` trick in `insert_data.sh` keeps the team inserts clean since teams can appear in multiple games.

## The queries

`queries.sh` answers questions like:
- Total/average goals from winning teams
- Highest number of goals scored by one team in a game (it's 7, Germany vs Brazil)
- Which teams made the Eighth-Final in 2014
- Who won each tournament (Germany in 2014, France in 2018)
- Teams whose names start with "Co"
