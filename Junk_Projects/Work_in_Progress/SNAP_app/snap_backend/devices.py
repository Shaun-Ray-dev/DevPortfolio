# Device CRUD operations

from snap_backend.db import get_connection

def add_device(hostname, ip_address, role="unknown", model=None, location=None):
    """
    Inserts a device into the devices table.
    Returns the device_id of the newly inserted row.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO devices (hostname, ip_address, role, model, location)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING device_id;
        """, (hostname, ip_address, role, model, location))
        device_id = cur.fetchone()[0]
        conn.commit()
        return device_id
    except Exception as e:
        print(f"[!] Failed to add device {hostname}: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()
