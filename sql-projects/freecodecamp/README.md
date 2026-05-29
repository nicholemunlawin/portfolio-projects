# 🌌 Universe Database

A PostgreSQL database project that models a simplified universe system containing galaxies, stars, planets, moons, and black holes.

This project was created using PostgreSQL and exported as a `.sql` database dump file. It is ideal for practicing:

- SQL database design
- Table relationships
- Primary and foreign keys
- PostgreSQL database restoration
- Query writing and data exploration

---

# 📁 Project Structure

```bash
.
├── universe.sql
└── README.md
```

---

# 🛠 Technologies Used

- PostgreSQL 12
- SQL
- pg_dump

---

# 🗄 Database Overview

The database contains the following main entities:

| Table | Description |
|---|---|
| `galaxy` | Stores information about galaxies |
| `star` | Stores stars belonging to galaxies |
| `planet` | Stores planets orbiting stars |
| `moon` | Stores moons orbiting planets |
| `blackhole` | Stores black hole data |

---

# 🔗 Entity Relationships

```text
Galaxy
  └── Star
        └── Planet
              └── Moon
```

### Relationship Details

- One galaxy can contain many stars
- One star can contain many planets
- One planet can contain many moons

---

# 🧱 Database Schema

## Galaxy Table

| Column | Type |
|---|---|
| galaxy_id | integer |
| name | varchar(50) |
| has_life | boolean |
| galaxy_type | varchar(50) |
| distance_from_earth | integer |

---

## Star Table

| Column | Type |
|---|---|
| star_id | integer |
| name | varchar(50) |
| distance_from_earth | numeric(15,2) |
| age_in_millions_of_years | integer |
| galaxy_id | integer |
| star_type | varchar(50) |

---

## Planet Table

| Column | Type |
|---|---|
| planet_id | integer |
| name | varchar(50) |
| description | text |
| has_life | boolean |
| is_spherical | boolean |
| star_id | integer |

---

## Moon Table

| Column | Type |
|---|---|
| moon_id | integer |
| name | varchar(50) |
| planet_id | integer |
| distance_from_earth | numeric(15,2) |
| is_spherical | boolean |

---

## Blackhole Table

| Column | Type |
|---|---|
| blackhole_id | integer |
| name | varchar(50) |
| distance_from_earth | integer |

---

# 🚀 Getting Started

## 1. Install PostgreSQL

Download PostgreSQL from:

- https://www.postgresql.org/download/

---

## 2. Create the Database

Open your terminal or PostgreSQL shell and run:

```bash
createdb universe
```

---

## 3. Import the SQL File

```bash
psql -U postgres -d universe -f universe.sql
```

Replace `postgres` with your PostgreSQL username if needed.

---

# ✅ Verify the Tables

After importing, connect to PostgreSQL:

```bash
psql -U postgres -d universe
```

Then run:

```sql
\dt
```

You should see tables similar to:

```text
blackhole
galaxy
moon
planet
star
```

---

# 🔍 Example Queries

## View All Galaxies

```sql
SELECT * FROM galaxy;
```

## View All Stars With Their Galaxy

```sql
SELECT star.name AS star_name,
       galaxy.name AS galaxy_name
FROM star
JOIN galaxy
ON star.galaxy_id = galaxy.galaxy_id;
```

## View Planets and Their Stars

```sql
SELECT planet.name AS planet_name,
       star.name AS star_name
FROM planet
JOIN star
ON planet.star_id = star.star_id;
```

## View Moons and Their Planets

```sql
SELECT moon.name AS moon_name,
       planet.name AS planet_name
FROM moon
JOIN planet
ON moon.planet_id = planet.planet_id;
```

---

# 🎯 Learning Objectives

This project demonstrates:

- Relational database design
- One-to-many relationships
- SQL table creation
- Primary and foreign key constraints
- PostgreSQL backup and restore workflow
- Basic SQL joins and queries

---

# 📚 Possible Improvements

Future enhancements could include:

- Adding asteroid tables
- Adding comet data
- Creating indexes for performance
- Adding advanced constraints
- Building a frontend application
- Creating stored procedures and views

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 📄 License

This project is open-source and available under the MIT License.

---

# 👨‍💻 Author

Created as a PostgreSQL database practice project.

