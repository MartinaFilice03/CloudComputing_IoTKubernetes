import psycopg2
import os
import random
import time

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

while True:
    try:
        conn = get_connection()
        cur = conn.cursor()

        device_id = random.randint(1, 5)
        value = round(random.uniform(20.0, 30.0), 2)

        cur.execute(
            "INSERT INTO temperatures (device_id, value) VALUES (%s, %s)",
            (device_id, value)
        )

        conn.commit()
        cur.close()
        conn.close()

        print(f"Inserted temperature {value} from device {device_id}")

    except Exception as e:
        print("Error:", e)

    time.sleep(3)