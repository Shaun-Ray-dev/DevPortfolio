import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="snapdb",
    user="postgres",
    password="postgres"  # <-- use your actual password
)
cursor = conn.cursor()

# Insert a test config for device_id = 1
cursor.execute("""
INSERT INTO configs (device_id, config_text, created_at)
VALUES (%s, %s, NOW())
""", (1, "hostname TestDevice\ninterface Gi0/1\nip address 192.168.1.100 255.255.255.0"))

conn.commit()

# Verify insertion
cursor.execute("SELECT * FROM configs WHERE device_id=%s", (1,))
print(cursor.fetchall())

# Close connection
cursor.close()
conn.close()
