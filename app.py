from flask import Flask, request, render_template
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)

def get_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            connection_timeout=10
        )
    except Exception as e:
        print("DB connection error:", e)
        return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    db = None
    cursor = None

    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # validation
        if not username or not password:
            return render_template(
                "index.html",
                message="⚠️ Username and password cannot be empty",
                status="error"
            )

        # hash password (important)
        hashed_password = generate_password_hash(password)

        db = get_db()
        if db is None:
            return render_template(
                "index.html",
                message="❌ Database connection failed",
                status="error"
            )

        cursor = db.cursor()

        sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
        cursor.execute(sql, (username, hashed_password))
        db.commit()

        return render_template(
            "index.html",
            message="✅ User added successfully!",
            status="success"
        )

    except Exception as e:
        return render_template(
            "index.html",
            message=f"❌ Error: {str(e)}",
            status="error"
        )

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)