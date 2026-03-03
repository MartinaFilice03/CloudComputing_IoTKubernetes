from flask import Flask, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

# Questa rotta serve solo a caricare la pagina iniziale
@app.route("/")
def index():
    return render_template("index.html")

# Questa rotta "API" restituisce solo i dati
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

    # Trasformiamo i dati in una lista di dizionari (JSON)
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "device": r[1],
            "value": r[2],
            "timestamp": str(r[3])
        })
    return jsonify(data)