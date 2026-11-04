import os
import threading
import webbrowser
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_ticket_db")
    )

def fetch_all(query, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def call_procedure(name, args):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.callproc(name, args)
        conn.commit()
    finally:
        cur.close()
        conn.close()

@app.route("/")
def index():
    return dashboard()

@app.route("/movies")
def movies_page():
    return dashboard(manage_only=True)

def dashboard(manage_only=False):
    try:
        stats = fetch_all("""
            SELECT COUNT(*) AS total,
                   SUM(status='Active') AS active,
                   SUM(status='Inactive') AS inactive
            FROM movies
        """)[0]
        movies = fetch_all("SELECT * FROM movies ORDER BY movie_id DESC")
        return render_template(
            "index.html",
            stats=stats,
            movies=movies,
            search="",
            manage_only=manage_only
        )
    except Error as e:
        return render_template("error.html", error=str(e)), 500

@app.route("/search")
def search():
    term = request.args.get("q", "").strip()
    manage_only = request.args.get("view") == "movies"
    try:
        movies = fetch_all(
            "SELECT * FROM movies WHERE title LIKE %s OR genre LIKE %s ORDER BY movie_id DESC",
            (f"%{term}%", f"%{term}%")
        )
        stats = fetch_all("""
            SELECT COUNT(*) AS total,
                   SUM(status='Active') AS active,
                   SUM(status='Inactive') AS inactive
            FROM movies
        """)[0]
        return render_template(
            "index.html",
            stats=stats,
            movies=movies,
            search=term,
            manage_only=manage_only
        )
    except Error as e:
        return render_template("error.html", error=str(e)), 500

@app.route("/add", methods=["POST"])
def add_movie():
    try:
        call_procedure("sp_add_movie", (
            request.form["title"].strip(),
            request.form["genre"].strip(),
            Decimal(request.form["price"]),
            request.form.get("duration") or None,
            request.form.get("language", "").strip() or "English"
        ))
        flash("Movie added successfully.", "success")
    except Exception as e:
        flash(f"Could not add movie: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/update/<int:movie_id>", methods=["POST"])
def update_movie(movie_id):
    try:
        call_procedure("sp_update_movie", (
            movie_id,
            request.form["title"].strip(),
            request.form["genre"].strip(),
            Decimal(request.form["price"]),
            request.form.get("duration") or None,
            request.form.get("language", "").strip() or "English"
        ))
        flash("Movie details updated.", "success")
    except Exception as e:
        flash(f"Could not update movie: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/delete/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    try:
        call_procedure("sp_delete_movie", (movie_id,))
        flash("Movie deleted successfully.", "success")
    except Exception as e:
        flash(f"Could not delete movie: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/toggle/<int:movie_id>", methods=["POST"])
def toggle_status(movie_id):
    try:
        call_procedure("sp_toggle_movie_status", (movie_id,))
        flash("Movie status changed.", "success")
    except Exception as e:
        flash(f"Could not change status: {e}", "danger")
    return redirect(url_for("index"))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
