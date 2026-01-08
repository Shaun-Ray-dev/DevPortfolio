import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="snapdb",
    user="postgres",
    password="postgres"  # <-- put your PostgreSQL password here
)

cursor = conn.cursor()

# Add a test device
cursor.execute("""
INSERT INTO devices (hostname, ip_address, model, location, role)
VALUES (%s, %s, %s, %s, %s)
""", ("TestDevice", "192.168.1.100", "Cisco 9000", "Lab", "Switch"))

conn.commit()

# Verify it was added
cursor.execute("SELECT * FROM devices WHERE hostname=%s", ("TestDevice",))
print(cursor.fetchall())

# Close the connection
cursor.close()
conn.close()


