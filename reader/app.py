from flask import Flask, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

#This route is only used to load the home page
@app.route("/")
def index():
    return render_template("index.html")

#This "API" route only returns data
@app.route("/api/temperatures")
def get_temperatures():
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT id, device_id, value, created_at FROM temperatures ORDER BY created_at DESC LIMIT 20;")
    rows = cur.fetchall()
    conn.close()

    #Transform the data into a list of dictionaries (JSON)
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "device": r[1],
            "value": r[2],
            "timestamp": str(r[3])
        })
    return jsonify(data)