from devices import add_device
from subnet_calc import get_usable_ips
from configs import add_config
from db import get_connection
import random
import ipaddress

# --- Universal roles and device counts ---
roles = {
    "router": 1,
    "switch": 2,
    "server": 2,
    "ip_phone": 5,
    "client": 10
}

# -----------------------------
# Step 1: Generate Topology
# -----------------------------
def generate_topology(subnets):
    topology = {}
    router_counter = 1

    for idx, subnet in enumerate(subnets, start=1):
        if not isinstance(subnet, ipaddress.IPv4Network):
            print(f"[!] Warning: {subnet} is not a valid IPv4Network, skipping...")
            continue

        usable_ips = get_usable_ips(str(subnet.network_address), subnet.prefixlen)
        if not usable_ips:
            print(f"[!] Warning: Subnet {subnet} has no usable IPs, skipping...")
            continue

        subnet_name = f"subnet_{idx}"
        topology[subnet_name] = {
            "network": str(subnet),
            "router": None,
            "switches": []
        }

        ip_index = 0

        # --- Add router ---
        if ip_index >= len(usable_ips):
            print(f"[!] Warning: Subnet {subnet} ran out of IPs before router could be assigned")
            continue
        router_ip = usable_ips[ip_index]
        router_hostname = f"Router{router_counter}"
        add_device(router_hostname, router_ip, role="router")
        topology[subnet_name]["router"] = {"hostname": router_hostname, "ip": router_ip}
        ip_index += 1
        router_counter += 1

        # --- Add switches ---
        num_switches = roles.get("switch", 1)
        for s in range(num_switches):
            if ip_index >= len(usable_ips):
                print(f"[!] Warning: Subnet {subnet} ran out of IPs before all switches could be assigned")
                break
            switch_ip = usable_ips[ip_index]
            switch_hostname = f"Switch{s+1}_Subnet{idx}"
            add_device(switch_hostname, switch_ip, role="switch")
            ip_index += 1
            topology[subnet_name]["switches"].append({"hostname": switch_hostname, "ip": switch_ip, "devices": []})

        # --- Add clients, servers, IP phones ---
        for role_name in ["server", "client", "ip_phone"]:
            count = roles.get(role_name, 0)
            for c in range(count):
                if ip_index >= len(usable_ips):
                    print(f"[!] Warning: Subnet {subnet} ran out of IPs before all {role_name}s could be assigned")
                    break
                host_ip = usable_ips[ip_index]
                hostname = f"{role_name.capitalize()}{c+1}_Subnet{idx}"
                add_device(hostname, host_ip, role=role_name)
                ip_index += 1
                # Assign devices: IP phones to first switch, others randomly
                if topology[subnet_name]["switches"]:
                    if role_name == "ip_phone":
                        switch = topology[subnet_name]["switches"][0]
                    else:
                        switch = random.choice(topology[subnet_name]["switches"][1:] or topology[subnet_name]["switches"])
                    switch["devices"].append({"hostname": hostname, "ip": host_ip})

    return topology

# -----------------------------
# Step 2: Provision Network Configs
# -----------------------------
def provision_network(topology):
    conn = get_connection()
    cur = conn.cursor()

    for subnet_name, subnet_data in topology.items():
        network_cidr = subnet_data["network"]
        network_ip, prefix = network_cidr.split('/')
        prefix = int(prefix)
        router = subnet_data.get("router")
        switches = subnet_data.get("switches", [])

        # --- Router Config ---
        if router:
            hostname = router["hostname"]
            router_ip = router["ip"]
            config_lines = [f"hostname {hostname}"]
            config_lines.append(f"interface Gig0/0\n ip address {router_ip} {prefix}\n no shutdown\n")

            # Static routes to other subnets
            for other_subnet_name, other_data in topology.items():
                if other_subnet_name == subnet_name:
                    continue
                next_hop_router = other_data.get("router")
                if next_hop_router:
                    next_hop_ip = next_hop_router["ip"]
                    config_lines.append(f"ip route {other_data['network']} {next_hop_ip}")

            config_text = "\n".join(config_lines)
            cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (hostname,))
            row = cur.fetchone()
            if row:
                device_id = row[0]
                add_config(device_id, config_text)
            else:
                print(f"[!] Error: Device '{hostname}' not found in DB, skipping config")

        # --- Switch Configs ---
        for switch in switches:
            hostname = switch["hostname"]
            switch_ip = switch["ip"]
            config_lines = [
                f"hostname {hostname}",
                f"interface Vlan1\n ip address {switch_ip} {prefix}\n no shutdown",
                "spanning-tree mode rapid-pvst"
            ]
            config_text = "\n".join(config_lines)
            cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (hostname,))
            row = cur.fetchone()
            if row:
                device_id = row[0]
                add_config(device_id, config_text)
            else:
                print(f"[!] Error: Switch '{hostname}' not found in DB, skipping config")

            # --- End Devices ---
            for device in switch.get("devices", []):
                d_hostname = device["hostname"]
                d_ip = device["ip"]
                config_text = f"hostname {d_hostname}\nip address {d_ip} {prefix}\n!"
                cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (d_hostname,))
                row = cur.fetchone()
                if row:
                    device_id = row[0]
                    add_config(device_id, config_text)
                else:
                    print(f"[!] Error: Device '{d_hostname}' not found in DB, skipping config")

    conn.commit()
    cur.close()
    conn.close()
    print("[✓] Network provisioning complete: all devices and configs saved.")

# -----------------------------
# Step 3: Convenience function
# -----------------------------
def assign_and_provision(subnets):
    topology = generate_topology(subnets)
    provision_network(topology)
    return topology

# -----------------------------
# Step 4: End-to-end test block
# -----------------------------
if __name__ == "__main__":
    test_subnets = [
        ipaddress.IPv4Network("192.168.10.0/28"),
        ipaddress.IPv4Network("192.168.20.0/29")
    ]
    print("[*] Running end-to-end SNAP test...")
    topology = assign_and_provision(test_subnets)
    print("[*] Test complete. Topology generated:")
    for sn, data in topology.items():
        print(f"{sn}: {data}")



def generate_device_config(device):
    """
    Generate a basic config for device based on role
    """
    role = device.get("role", "unknown")
    hostname = device["hostname"]
    ip = device["ip"]

    config_lines = [f"hostname {hostname}"]

    if role == "router":
        config_lines.append(f"interface Gig0/0\n ip address {ip} 255.255.255.0\n no shutdown")
        # Routing placeholder (dynamic later)
    elif role == "switch":
        config_lines.append(f"interface Vlan1\n ip address {ip} 255.255.255.0\n no shutdown")
        config_lines.append("spanning-tree mode rapid-pvst")
    else:  # end devices
        config_lines.append(f"ip address {ip} 255.255.255.0\n!")

    return "\n".join(config_lines)

