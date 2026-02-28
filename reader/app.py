from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT id, device_id, value, created_at
        FROM temperatures
        ORDER BY created_at DESC
        LIMIT 20;
    """)
    rows = cur.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>IoT Temperature Dashboard</title>
        <style>
            body {
                font-family: Arial;
                background-color: #f4f6f8;
                text-align: center;
            }
            table {
                margin: auto;
                border-collapse: collapse;
                width: 70%;
                background: white;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #2c3e50;
                color: white;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            h1 {
                margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <h1>🌡 IoT Temperature Dashboard</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Device</th>
                <th>Temperature (°C)</th>
                <th>Timestamp</th>
            </tr>
    """

    for row in rows:
        html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)