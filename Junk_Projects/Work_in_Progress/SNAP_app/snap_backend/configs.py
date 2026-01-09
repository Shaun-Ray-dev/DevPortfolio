# Config CRUD operations
# from .db import get_connection

# snap_backend/configs.py
# Config CRUD operations
from snap_backend.db import get_connection
from datetime import datetime

def add_config(device_id, config_data):
    """
    Inserts a config for a device into the configs table.
    """
    if not device_id:
        print("[!] Invalid device_id; cannot add config.")
        return None

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO configs (device_id, config_text, created_at)
            VALUES (%s, %s, %s)
            RETURNING config_id;
        """, (device_id, config_data, datetime.now()))
        config_id = cur.fetchone()[0]
        conn.commit()
        return config_id
    except Exception as e:
        print(f"[!] Failed to add config for device_id {device_id}: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()


def list_configs(device_id):
    """
    Returns a list of configs for a given device_id.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT config_id, config_text, created_at FROM configs WHERE device_id=%s;", (device_id,))
        rows = cur.fetchall()
        return [{"config_id": r[0], "config": r[1], "created_at": r[2]} for r in rows]
    finally:
        cur.close()
        conn.close()










# from snap_backend.db import get_connection
# from datetime import datetime

# def add_config(device_id, config_data):
#     """
#     Inserts a config for a device into the configs table.
#     """
#     if not device_id:
#         print("[!] Invalid device_id; cannot add config.")
#         return None

#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("""
#             INSERT INTO configs (device_id, config, created_at)
#             VALUES (%s, %s, %s)
#             RETURNING config_id;
#         """, (device_id, config_data, datetime.now()))
#         config_id = cur.fetchone()[0]
#         conn.commit()
#         return config_id
#     except Exception as e:
#         print(f"[!] Failed to add config for device_id {device_id}: {e}")
#         conn.rollback()
#         return None
#     finally:
#         cur.close()
#         conn.close()


# def list_configs(device_id):
#     """
#     Returns a list of configs for a given device_id.
#     """
#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT config_id, config, created_at FROM configs WHERE device_id=%s;", (device_id,))
#         rows = cur.fetchall()
#         return [{"config_id": r[0], "config": r[1], "created_at": r[2]} for r in rows]
#     finally:
#         cur.close()
#         conn.close()
