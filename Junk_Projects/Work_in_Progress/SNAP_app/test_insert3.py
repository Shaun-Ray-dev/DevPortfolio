from snap_backend.db import get_connection

def insert_device(conn, hostname, ip, model, location, role):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO devices (hostname, ip_address, model, location, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING device_id;
        """, (hostname, ip, model, location, role))
        device_id = cur.fetchone()[0]
    conn.commit()
    return device_id

def insert_config(conn, device_id, config_text):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO configs (device_id, config_text, created_at)
            VALUES (%s, %s, NOW())
            RETURNING config_id, created_at;
        """, (device_id, config_text))
        row = cur.fetchone()
    conn.commit()
    return row

def main():
    conn = get_connection()

    # Test device
    device_id = insert_device(conn, "TestDevice3", "192.168.1.103", "Cisco 9500", "Lab3", "Switch")
    print(f"Device added with ID: {device_id}")

    # Test config for the device
    cfg = insert_config(conn, device_id, "interface Gig0/2\n ip address 192.168.1.103 255.255.255.0\n no shutdown")
    print(f"Config added with ID: {cfg[0]}, Created at: {cfg[1]}")

    conn.close()

if __name__ == "__main__":
    main()
