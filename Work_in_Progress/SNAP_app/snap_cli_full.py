"""
SNAP CLI Full: Technician Mode
- Input ISP network info
- Calculate subnets
- Discover devices
- Map topology
- Assign IPs and store devices in DB
- Backup configs
- Generate and dry-run push configs
- Export full topology and configs
"""

import ipaddress
import os
import json

from snap_backend import vault
from snap_backend import subnet_calc
from snap_backend.discovery_enhanced import discover_and_map
from snap_backend.netmiko_wrapper import connect_device, disconnect_device, push_config, backup_config
from snap_backend.devices import add_device
from snap_backend.configs import add_config
from snap_backend.snap_engine import generate_device_config

# -----------------------------
# Step 0: Get ISP Network Info
# -----------------------------
def get_network_input():
    while True:
        network_str = input("Enter the network from ISP (e.g., 203.0.113.0/24): ").strip()
        try:
            network = ipaddress.ip_network(network_str, strict=False)
            break
        except ValueError:
            print("[!] Invalid network. Try again.")

    while True:
        try:
            num_subnets = int(input("Number of subnets required: ").strip())
            if num_subnets <= 0: raise ValueError
            break
        except ValueError:
            print("[!] Enter a positive integer.")

    while True:
        try:
            hosts_per_subnet = int(input("Hosts per subnet: ").strip())
            if hosts_per_subnet <= 0: raise ValueError
            break
        except ValueError:
            print("[!] Enter a positive integer.")

    return network, num_subnets, hosts_per_subnet

# -----------------------------
# Step 1: Calculate Subnets
# -----------------------------
def calculate_subnets(network, num_subnets, hosts_per_subnet):
    required_hosts = hosts_per_subnet + 2
    new_prefix = 32 - (required_hosts - 1).bit_length()
    all_subnets = list(network.subnets(new_prefix=new_prefix))
    if len(all_subnets) < num_subnets:
        print(f"[!] Only {len(all_subnets)} subnets possible.")
    return all_subnets[:num_subnets]

# -----------------------------
# Step 2: Discover Devices & Map
# -----------------------------
def discover_devices(subnets):
    all_devices = []
    for sn in subnets:
        print(f"\n[*] Discovering devices in subnet {sn}")
        devices = discover_and_map(str(sn), vault)
        all_devices.extend(devices)
    return all_devices

# -----------------------------
# Step 3: Assign IPs to Devices
# -----------------------------
def assign_ips(devices, subnets):
    for subnet in subnets:
        usable_ips = subnet_calc.get_usable_ips(str(subnet.network_address), subnet.prefixlen)
        for idx, device in enumerate(devices):
            if idx < len(usable_ips):
                ip = usable_ips[idx]
                device["ip"] = ip
                add_device(device["hostname"], ip, role=device.get("role", "unknown"), model=device.get("model"))
    return devices

# -----------------------------
# Step 4: Backup & Push Configs
# -----------------------------
def backup_and_push(devices, dry_run=True):
    for device in devices:
        ip = device["ip"]
        print(f"\n--- Connecting to {ip} ---")
        device_info = {
            "device_type": "cisco_ios",
            "host": ip,
            "username": vault.get_credential("SNAP_ADMIN_USER"),
            "password": vault.get_credential("SNAP_ADMIN_PASS"),
            "secret": vault.get_credential("SNAP_ENABLE_PASS")
        }
        conn = connect_device(device_info)
        if not conn:
            print(f"[!] Could not connect to {ip}")
            continue

        # Backup
        config_backup = backup_config(conn)
        if config_backup:
            add_config(device["device_id"], config_backup)

        # Generate and dry-run push config
        config_text = generate_device_config(device)
        success = push_config(conn, config_text.splitlines(), dry_run=dry_run)
        print(f"Config push dry-run result: {success}")

        disconnect_device(conn)

# -----------------------------
# Step 5: Export Topology & Configs
# -----------------------------
def export_topology(devices):
    desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')
    folder_name = "SNAP_Full_Topology"
    folder_path = os.path.join(desktop, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    data = []
    for d in devices:
        data.append({
            "hostname": d["hostname"],
            "ip": d.get("ip"),
            "model": d.get("model"),
            "role": d.get("role")
        })

    # JSON
    json_path = os.path.join(folder_path, "topology.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[✓] Topology exported to {json_path}")

# -----------------------------
# Step 6: Main CLI Flow
# -----------------------------
if __name__ == "__main__":
    print("=== SNAP CLI Full Technician Mode ===\n")

    network, num_subnets, hosts_per_subnet = get_network_input()
    subnets = calculate_subnets(network, num_subnets, hosts_per_subnet)
    if not subnets:
        print("[!] Could not calculate subnets. Exiting.")
        exit(1)

    devices = discover_devices(subnets)
    devices = assign_ips(devices, subnets)
    backup_and_push(devices, dry_run=True)
    export_topology(devices)

    print("\n[✓] SNAP Full CLI workflow complete.")
