CREATE TABLE IF NOT EXISTS temperatures (
    id SERIAL PRIMARY KEY,
    device_id INT,
    value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
