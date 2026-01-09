"""
snap_orchestrator.py
Safe SNAP orchestration script for testing discovery and device backup/push.
- Scans subnet for devices
- Connects using Netmiko
- Backs up running config
- Dry-run config push
- Uses vault.py for credentials
"""

from snap_backend.discovery_enhanced import discover_and_map
from snap_backend import netmiko_wrapper as nw
from snap_backend import vault
import json

# ---------- CONFIG ----------
SUBNET = "172.25.64.0/24"  # adjust to your lab subnet
DRY_RUN = True             # True = config push won't actually change device

# ---------- DISCOVER DEVICES ----------
print(f"Scanning subnet {SUBNET} ...")
devices = discover_and_map(SUBNET, vault)
print(f"Found {len(devices)} device(s):")
print(json.dumps(devices, indent=2))

# ---------- LOOP OVER DEVICES ----------
for d in devices:
    ip = d["ip"]
    print(f"\n--- Processing {ip} ---")

    # Build device_info using vault
    device_info = {
        "device_type": "cisco_ios",  # adjust if using a different vendor
        "host": ip,
        "username": vault.get_credential("SNAP_ADMIN_USER"),
        "password": vault.get_credential("SNAP_ADMIN_PASS"),
        "secret": vault.get_credential("SNAP_ENABLE_PASS"),
    }

    # Connect
    conn = nw.connect_device(device_info)
    if not conn:
        print(f"Failed to connect to {ip}, skipping...")
        continue

    # Backup config
    config = nw.backup_config(conn)
    if config:
        print(f"Backup for {ip} (first 500 chars):\n{config[:500]}")

    # Dry-run push
    success = nw.push_config(conn, ["hostname SNAP_TEST"], dry_run=DRY_RUN)
    print(f"Dry-run push result: {success}")

    # Disconnect
    nw.disconnect_device(conn)

print("\nSNAP orchestration test complete.")
