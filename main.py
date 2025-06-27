from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_NAME = "Stamp"
DB_USER = "postgres"
DB_PASSWORD = "AM_IT"


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        entered_username = request.form["username"]
        entered_password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (entered_username,))
        result = cur.fetchone()

        cur.close()
        conn.close()

        if result and check_password_hash(result[0], entered_password):
            return redirect(url_for("success"))
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]

        hashed_password = generate_password_hash(new_password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                        (new_username, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("login"))
        except psycopg2.Error:
            conn.rollback()
            cur.close()
            conn.close()
            error = "Username already exists or error occurred."

    return render_template("Create.html", error=error)


@app.route("/success")
def success():
    return render_template("Success.html")


if __name__ == "__main__":
    app.run(debug=True)