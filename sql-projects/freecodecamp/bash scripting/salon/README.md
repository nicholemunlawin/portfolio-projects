# Salon Appointment Scheduler

This is a bash script for freeCodeCamp's relational database certification. Customers can book appointments at a salon by selecting a service, providing their phone number, and choosing a time.

## Tech Stack

- Bash
- PostgreSQL

## How to Run

First, create the database by running the SQL file against postgres:

```bash
psql --username=freecodecamp --dbname=postgres < salon.sql
```

Then make the script executable and run it:

```bash
chmod +x salon.sh
./salon.sh
```

## What It Does

- Shows a numbered list of available services
- Asks for the customer's phone number
- If the phone number isn't in the database, asks for their name and creates a new record
- Books the appointment with the selected time
- Confirms the booking with service name, time, and customer name

If someone picks a service that doesn't exist, it shows an error and asks them to pick again.

## Database

Three tables: `services`, `customers`, and `appointments`. Customers are looked up by phone number, and appointments reference both customer and service IDs.


