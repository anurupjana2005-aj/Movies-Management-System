# Movie Ticket Booking System — Admin Module

A beginner-friendly admin dashboard built with **Python Flask, MySQL and MySQL Stored Procedures**. It manages the movie catalogue only; customer registration, ticket booking and payment are outside this admin-only mini-project.

## Features
- Dashboard: total, active and inactive movie counts
- Add, edit and delete movie records
- Search by movie title or genre
- Activate/deactivate movies
- MySQL stored procedures for insert, update, delete and status changes

## Requirements
- Python 3.10+
- MySQL Server
- MySQL Workbench (used to run SQL scripts and view tables)

> MySQL Workbench is the database client. Make sure **MySQL Server** is installed and running too.

## 1. Create database and stored procedures
1. Open MySQL Workbench and connect to your local MySQL connection.
2. Open `sql/schema.sql`, click the lightning bolt (Execute), and wait for completion.
3. Open `sql/procedures.sql` and execute it.
4. Refresh the Schemas panel. You should see `movie_ticket_db` → Tables → `movies` and Stored Procedures.

## 2. Configure Python app
Open the project folder in VS Code / terminal. Create a file named exactly `.env` in the same folder as `app.py` (copy `.env.example` and rename it).

Example:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
DB_NAME=movie_ticket_db
FLASK_SECRET_KEY=my-local-secret
```
If your MySQL root account has no password, leave `DB_PASSWORD=` blank. Do not share your database password.

## 3. Install and run
```bash
python3 -m pip install -r requirements.txt
python3 app.py
```
Open the local address printed in the terminal, normally `http://127.0.0.1:5000`.

## Common problems
- **Can't connect / Access denied:** check MySQL Server is running and DB_USER / DB_PASSWORD in `.env` match your Workbench connection.
- **Unknown database:** execute `sql/schema.sql` first.
- **Procedure does not exist:** execute `sql/procedures.sql` after schema creation.
- **Workbench opens but app cannot connect:** Workbench is only a client; the MySQL Server service must be running.

## Project structure
```text
Movie_Ticket_Booking_Admin_MySQL/
├── app.py
├── sql/
│   ├── schema.sql
│   └── procedures.sql
├── templates/
│   ├── index.html
│   └── error.html
├── static/
│   ├── style.css
│   └── app.js
├── .env.example
├── requirements.txt
└── README.md
```
