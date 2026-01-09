from snap_backend import netmiko_wrapper as nw

test_device = {
    "device_type": "cisco_ios",   # adjust to your device type
    "host": "172.25.64.1",
    "username": "admin",
    "password": "password",
    "secret": "enablepassword",   # optional
}

conn = nw.connect_device(test_device)
if conn:
    print(f"Connected to {conn.host}")
    config = nw.backup_config(conn)
    print(config[:500])  # print first 500 chars
    nw.disconnect_device(conn)
else:
    print("Connection failed")
