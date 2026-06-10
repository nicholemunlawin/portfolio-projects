Student Database Project
Overview
This project contains a PostgreSQL database called students that stores information about students, majors, courses, and the relationships between them.
The database was created to practice database design concepts such as:
•	Table creation
•	Primary and foreign keys
•	One-to-many relationships
•	Many-to-many relationships
•	Data insertion and management
•	PostgreSQL database restoration from SQL dumps
________________________________________
Database Structure
The database consists of four main tables:
1. Students
Stores student information.
Column	Data Type	Description
student_id	Integer	Unique student identifier
first_name	VARCHAR(50)	Student’s first name
last_name	VARCHAR(50)	Student’s last name
major_id	Integer	References the student’s major
gpa	Numeric(2,1)	Student GPA
________________________________________
2. Majors
Stores the list of academic majors.
Column	Data Type	Description
major_id	Integer	Unique major identifier
major	VARCHAR(50)	Major name
________________________________________
3. Courses
Stores available courses.
Column	Data Type	Description
course_id	Integer	Unique course identifier
course	VARCHAR(100)	Course name
________________________________________
4. Majors_Courses
Junction table that connects majors and courses.
Column	Data Type
major_id	Integer
course_id	Integer
This table creates a many-to-many relationship between majors and courses.
________________________________________
Entity Relationship Overview
Students
    |
    | many-to-one
    v
Majors
    |
    | many-to-many
    v
Majors_Courses
    ^
    |
Courses
________________________________________
Relationships
Primary Keys
•	students.student_id
•	majors.major_id
•	courses.course_id
•	majors_courses (major_id, course_id)
Foreign Keys
•	students.major_id → majors.major_id
•	majors_courses.major_id → majors.major_id
•	majors_courses.course_id → courses.course_id
________________________________________
Sample Data
The database includes sample records for:
•	30+ students
•	Multiple academic majors
•	Multiple courses
•	Major-course mappings
Example student record:
INSERT INTO public.students
VALUES (33, 'Dejon', 'Howell', 37, 4.0);
________________________________________
Requirements
•	PostgreSQL 12+
•	pgAdmin (optional)
•	psql command-line tool
________________________________________
Restoring the Database
Using psql
psql -U postgres -f students.sql
Using pgAdmin
1.	Open pgAdmin.
2.	Create or connect to a PostgreSQL server.
3.	Right-click Databases.
4.	Select Restore.
5.	Choose students.sql.
6.	Start the restore process.
________________________________________
Example Queries
View all students
SELECT * FROM students;
Find students with a GPA above 3.5
SELECT first_name, last_name, gpa
FROM students
WHERE gpa > 3.5;
Display students and their majors
SELECT
    s.first_name,
    s.last_name,
    m.major
FROM students s
LEFT JOIN majors m
ON s.major_id = m.major_id;
Count students per major
SELECT
    m.major,
    COUNT(s.student_id) AS total_students
FROM majors m
LEFT JOIN students s
ON m.major_id = s.major_id
GROUP BY m.major;
________________________________________
Learning Objectives
This project helped me practice:
•	PostgreSQL database management
•	Database normalization
•	Primary and foreign key implementation
•	Many-to-many relationship design
•	Writing SQL queries and joins
•	Importing and restoring SQL database dumps
________________________________________
Author
Created as part of a SQL/PostgreSQL database learning project and used for practicing relational database concepts.
