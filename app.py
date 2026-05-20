ffrom flask import Flask, request
import mysql.connector
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

@app.route('/')
def home():
    return '''
    <form method="POST" action="/register">
    Username:<input name="username"><br>
    Password:<input name="password"><br>
    <input type="submit">
    </form>
    '''

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    cursor = db.cursor()

    sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
    cursor.execute(sql, (username, password))
    db.commit()

    cursor.close()
    db.close()

    return "Data stored successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)