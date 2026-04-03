import psycopg2
import time
import random
import os

def insert_temperature():
    # Establish connection to the PostgreSQL service within the Kubernetes cluster
    # Credentials and host are pulled from environment variables and service names
    conn = psycopg2.connect(
        host="postgres-service",
        database="iot",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    # Ensure the target table exists before attempting insertion
    cur.execute("""
        CREATE TABLE IF NOT EXISTS temperatures (
            id SERIAL PRIMARY KEY,
            device_id INT,
            value FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Simulate IoT sensor data: random device ID (1-5) and temperature (20-30°C)
    device_id = random.randint(1, 5)
    value = round(random.uniform(20, 30), 2)

    cur.execute(
        "INSERT INTO temperatures (device_id, value) VALUES (%s, %s);",
        (device_id, value)
    )

    # Commit changes to make the transaction permanent and close connections
    conn.commit()
    conn.close()

while True:
    try:
        insert_temperature()
        print("Inserted temperature")
        time.sleep(3) # Wait 3 seconds before the next reading
    except Exception as e:
        # If the database is not ready or connection fails, log the error and retry
        print("Error:", e)
        time.sleep(5)