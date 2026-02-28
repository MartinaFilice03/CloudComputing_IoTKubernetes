from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")   # ← USA LA SECRET
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM temperatures ORDER BY id DESC LIMIT 10;")
    rows = cur.fetchall()

    html = "<h1>IoT Temperature Dashboard</h1><ul>"
    for row in rows:
        html += f"<li>ID: {row[0]} | Device: {row[1]} | Temp: {row[2]} | Time: {row[3]}</li>"
    html += "</ul>"

    cur.close()
    conn.close()

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)