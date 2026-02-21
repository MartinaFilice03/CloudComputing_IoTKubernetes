from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = "postgres-service"
DB_NAME = "iot"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    return "IoT Reader Running"

@app.route("/temperatures")
def get_temperatures():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM temperatures ORDER BY created_at DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)