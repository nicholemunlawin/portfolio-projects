# Periodic Table Database

A PostgreSQL database project for freeCodeCamp's Relational Database Certification. This project stores and queries element information from the periodic table.

## Project Structure

```
periodic_table/
├── element.sh              # Bash script to query element data
├── periodic_table.sql      # PostgreSQL database schema and data
└── .gitignore
```

## Database Schema

The database contains three tables:

- **elements** - Stores atomic number, symbol, and name
- **properties** - Stores atomic mass, melting/boiling points, and type
- **types** - Stores element types (metal, metalloid, nonmetal)

## Setup

### Prerequisites

- PostgreSQL installed and running
- `psql` command-line tool available

### Database Setup

1. Create the database and populate it:

```bash
psql -U postgres -f periodic_table.sql
```

### Running the Script

```bash
./element.sh <element>
```

Where `<element>` can be:
- Atomic number (e.g., `1`)
- Element symbol (e.g., `H`)
- Element name (e.g., `Hydrogen`)

### Examples

```bash
./element.sh 1
# The element with atomic number 1 is Hydrogen (H). It's a nonmetal, with a mass of 1.008 amu. Hydrogen has a melting point of -259.1 celsius and a boiling point of -252.9 celsius.

./element.sh Carbon
# The element with atomic number 6 is Carbon (C). It's a nonmetal, with a mass of 12.011 amu. Carbon has a melting point of 3550 celsius and a boiling point of 4027 celsius.
```

## Technologies Used

- PostgreSQL
- Bash

## License

This project is part of the freeCodeCamp curriculum.
