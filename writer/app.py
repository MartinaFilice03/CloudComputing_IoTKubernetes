import psycopg2
import time
import random
import os

def insert_temperature():
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    # CREA TABELLA SE NON ESISTE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id SERIAL PRIMARY KEY,
            device_id INT,
            value FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    device_id = random.randint(1, 5)
    value = round(random.uniform(20, 30), 2)

    cur.execute(
        "INSERT INTO temperatures (device_id, value) VALUES (%s, %s);",
        (device_id, value)
    )

    conn.commit()
    conn.close()

while True:
    try:
        insert_temperature()
        print("Inserted temperature")
        time.sleep(3)
    except Exception as e:
        print("Error:", e)
        time.sleep(5)