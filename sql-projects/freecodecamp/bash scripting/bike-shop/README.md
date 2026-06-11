# Bike Rental Shop

A command-line bike rental application I built as part of the freeCodeCamp Relational Database certification. It uses Bash for the interface and PostgreSQL for storing bike, customer, and rental data.

## What it does

- Rent a bike — picks from available inventory, creates a new customer if needed
- Return a bike — looks up rentals by phone number and marks them returned
- Tracks which bikes are currently out and which are available

## Database schema

Three tables: `bikes`, `customers`, and `rentals`. The SQL dump (`bike-shop.sql`) sets everything up with sample data — 9 bikes across Mountain, Road, and BMX types.

## Running it

Make sure PostgreSQL is running and the `bikes` database is set up:

```bash
psql -U postgres < bike-shop.sql
```

Then run the app:

```bash
chmod +x bike-shop.sh
./bike-shop.sh
```

The script connects as the `freecodecamp` user by default, so you'll need that user created in PostgreSQL or change the connection string in the script.

## Files

- `bike-shop.sh` — the main application
- `bike-shop.sql` — database setup and seed data
