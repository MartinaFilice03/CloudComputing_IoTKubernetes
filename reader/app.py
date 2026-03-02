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
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    text-align: center;
}

table {
    border-collapse: collapse;
    width: 80%;
    margin: 40px auto;
    table-layout: fixed; /* IMPORTANTE */
}

th, td {
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}

/* Forza larghezze precise per ogni colonna */
th:nth-child(1), td:nth-child(1) { width: 10%; }
th:nth-child(2), td:nth-child(2) { width: 10%; }
th:nth-child(3), td:nth-child(3) { width: 15%; }
th:nth-child(4), td:nth-child(4) { width: 65%; }

th {
    background-color: #2c3e50;
    color: white;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}
</style>
</head>
<body>

<h1>IoT Temperature Dashboard</h1>

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