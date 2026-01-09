# snap_backend/discovery_enhanced.py
"""
Enhanced device discovery:
- Uses nmap for live hosts
- Connects to devices via Netmiko
- Queries CDP (Cisco) or LLDP (other vendors) for neighbors
- Stores devices in DB
- Auto-adds discovered neighbors
"""

from snap_backend import discovery
from snap_backend import netmiko_wrapper as nw
from snap_backend.devices import add_device
from snap_backend.db import get_connection
import json
import re

# ---------------------------
# Neighbor parsers
# ---------------------------
def parse_cdp_neighbors(output):
    """
    Parses 'show cdp neighbors detail' output.
    Returns a list of neighbor dicts: {'hostname':..., 'ip':..., 'model':...}
    """
    neighbors = []
    entries = output.split("-------------------------")
    for entry in entries:
        hostname_match = re.search(r"Device ID: (.+)", entry)
        ip_match = re.search(r"IP address: ([\d\.]+)", entry)
        model_match = re.search(r"Platform: (\S+)", entry)
        if hostname_match and ip_match:
            neighbors.append({
                "hostname": hostname_match.group(1).strip(),
                "ip": ip_match.group(1).strip(),
                "model": model_match.group(1).strip() if model_match else None
            })
    return neighbors

def parse_lldp_neighbors(output):
    """
    Parses 'show lldp neighbors detail' output (generic for Juniper/Arista/etc.)
    Returns a list of neighbor dicts: {'hostname':..., 'ip':..., 'model':...}
    """
    neighbors = []
    entries = output.split("\n\n")  # LLDP blocks are separated by blank lines
    for entry in entries:
        hostname_match = re.search(r"System Name: (.+)", entry)
        ip_match = re.search(r"Management Address: ([\d\.]+)", entry)
        model_match = re.search(r"System Description: (.+)", entry)
        if hostname_match and ip_match:
            neighbors.append({
                "hostname": hostname_match.group(1).strip(),
                "ip": ip_match.group(1).strip(),
                "model": model_match.group(1).strip() if model_match else None
            })
    return neighbors

# ---------------------------
# Main discovery function
# ---------------------------
def discover_and_map(subnet, vault, device_type="cisco_ios"):
    """
    Scan subnet, connect to devices, discover neighbors and models.
    Returns a list of devices with full info.
    """
    live_hosts = discovery.scan_subnet(subnet)
    all_devices = []

    conn = get_connection()
    cur = conn.cursor()

    try:
        for host in live_hosts:
            ip = host["ip"]
            print(f"\n[+] Connecting to {ip}")

            device_info = {
                "device_type": device_type,
                "host": ip,
                "username": vault.get_credential("SNAP_ADMIN_USER"),
                "password": vault.get_credential("SNAP_ADMIN_PASS"),
                "secret": vault.get_credential("SNAP_ENABLE_PASS"),
            }

            net_conn = nw.connect_device(device_info)
            if not net_conn:
                print(f"[!] Could not connect to {ip}")
                continue

            # --- Main device model ---
            output = nw.run_command(net_conn, "show version")
            model = None
            if output:
                for line in output.splitlines():
                    if "Model" in line or "cisco" in line.lower():
                        model = line.strip()
                        break

            hostname = host.get("hostname") or f"Device_{ip}"

            # --- Add main device to DB if not exists ---
            cur.execute("SELECT device_id FROM devices WHERE ip_address=%s;", (ip,))
            row = cur.fetchone()
            if row:
                device_id = row[0]
            else:
                device_id = add_device(hostname=hostname, ip_address=ip, role="unknown", model=model)

            all_devices.append({
                "ip": ip,
                "hostname": hostname,
                "model": model,
                "device_id": device_id
            })

            # --- Discover neighbors ---
            neighbors = []

            # Try CDP first (Cisco)
            cdp_output = nw.run_command(net_conn, "show cdp neighbors detail")
            if cdp_output:
                neighbors = parse_cdp_neighbors(cdp_output)
            else:
                # Try LLDP (other vendors)
                lldp_output = nw.run_command(net_conn, "show lldp neighbors detail")
                if lldp_output:
                    neighbors = parse_lldp_neighbors(lldp_output)

            for n in neighbors:
                # Check if neighbor already exists
                cur.execute("SELECT device_id FROM devices WHERE ip_address=%s;", (n["ip"],))
                n_row = cur.fetchone()
                if n_row:
                    n_device_id = n_row[0]
                else:
                    n_device_id = add_device(hostname=n["hostname"], ip_address=n["ip"],
                                             role="unknown", model=n.get("model"))
                all_devices.append({
                    "ip": n["ip"],
                    "hostname": n["hostname"],
                    "model": n.get("model"),
                    "device_id": n_device_id
                })
                print(f"[i] Neighbor discovered: {n['hostname']} ({n['ip']})")

            nw.disconnect_device(net_conn)

    finally:
        conn.commit()
        cur.close()
        conn.close()

    return all_devices

# ---------------------------
# Quick test
# ---------------------------
if __name__ == "__main__":
    from snap_backend import vault
    subnet = "172.25.64.0/24"
    devices = discover_and_map(subnet, vault)
    print(json.dumps(devices, indent=2))


