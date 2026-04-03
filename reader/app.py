from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Main route to display the HTML dashboard
@app.route("/")
def dashboard():
    # Establish connection to the PostgreSQL service using environment variables for credentials
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()
    # Fetch the latest 20 temperature readings ordered by timestamp
    cur.execute("""
        SELECT id, device_id, value, created_at
        FROM temperatures
        ORDER BY created_at DESC
        LIMIT 20;
    """)

    rows = cur.fetchall()
    conn.close() # Always close the connection to free up database resources

    # Start building the HTML response with embedded CSS for styling
    html = """
    <html>
    <head>
    <title>IoT Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ecf0f1;
            text-align: center;
        }

        h1 {
            margin-top: 30px;
        }

        table {
            border-collapse: collapse;
            width: 70%;
            margin: 40px auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }

        th {
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            text-align: left;
        }

        td {
            padding: 12px 15px;
            text-align: left;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
    </head>
    <body>

    <h1>🌡️ IoT Temperature Dashboard</h1>

    <table>
        <tr>
            <th>ID</th>
            <th>Device</th>
            <th>Temperature (°C)</th>
            <th>Timestamp</th>
        </tr>
    """

    # Dynamically generate table rows from database records
    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
        </tr>
        """

    # Close the HTML tags
    html += """
    </table>

    </body>
    </html>
    """

    return html


# API Endpoint returning raw data in JSON-compatible list format (useful for debugging)
@app.route("/temperatures")
def temperatures():
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

    # Convert database rows (tuples) into lists for JSON serialization
    return [list(row) for row in rows]

# Run the Flask application on port 5000, accessible from all network interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)