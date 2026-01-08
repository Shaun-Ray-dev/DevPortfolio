# from snap_backend.devices import add_device
# from snap_backend.configs import add_config
# from snap_backend.db import get_connection

# import random
# import ipaddress
# import os
# import json

# # -----------------------------
# # Step 0: User Input Functions
# # -----------------------------
# def get_network_input():
#     while True:
#         network_str = input("Enter the network address from ISP (e.g. 203.0.113.0/24): ").strip()
#         try:
#             network = ipaddress.ip_network(network_str, strict=False)
#             break
#         except ValueError:
#             print("[!] Invalid network. Try again.")
    
#     while True:
#         try:
#             num_subnets = int(input("Enter number of subnets required: ").strip())
#             if num_subnets <= 0:
#                 raise ValueError
#             break
#         except ValueError:
#             print("[!] Enter a positive integer for number of subnets.")
    
#     while True:
#         try:
#             hosts_per_subnet = int(input("Enter number of hosts per subnet: ").strip())
#             if hosts_per_subnet <= 0:
#                 raise ValueError
#             break
#         except ValueError:
#             print("[!] Enter a positive integer for hosts per subnet.")
    
#     return network, num_subnets, hosts_per_subnet

# def calculate_subnets(network, num_subnets, hosts_per_subnet):
#     """
#     Returns a list of IPv4Network objects for the requested subnets.
#     Adjusts prefix to fit hosts per subnet.
#     """
#     required_hosts = hosts_per_subnet + 2  # account for network & broadcast
#     new_prefix = 32 - (required_hosts - 1).bit_length()
#     all_subnets = list(network.subnets(new_prefix=new_prefix))
    
#     if len(all_subnets) < num_subnets:
#         print(f"[!] Only {len(all_subnets)} subnets possible with the given parameters.")
#         return all_subnets[:len(all_subnets)]
    
#     return all_subnets[:num_subnets]

# # -----------------------------
# # Step 1: Roles
# # -----------------------------
# roles = {
#     "router": 1,
#     "switch": 2,
#     "server": 2,
#     "ip_phone": 5,
#     "client": 10
# }

# # -----------------------------
# # Step 2: Generate Topology
# # -----------------------------
# def generate_topology(subnets, get_usable_ips):
#     topology = {}
#     router_counter = 1

#     for idx, subnet in enumerate(subnets, start=1):
#         usable_ips = get_usable_ips(str(subnet.network_address), subnet.prefixlen)
#         if not usable_ips:
#             continue

#         subnet_name = f"subnet_{idx}"
#         topology[subnet_name] = {
#             "network": str(subnet),
#             "router": None,
#             "switches": []
#         }

#         ip_index = 0

#         # --- Add router ---
#         router_ip = usable_ips[ip_index]
#         router_hostname = f"Router{router_counter}"
#         add_device(router_hostname, router_ip, role="router")
#         topology[subnet_name]["router"] = {"hostname": router_hostname, "ip": router_ip}
#         ip_index += 1
#         router_counter += 1

#         # --- Add switches ---
#         num_switches = roles.get("switch", 1)
#         for s in range(num_switches):
#             if ip_index >= len(usable_ips):
#                 break
#             switch_ip = usable_ips[ip_index]
#             switch_hostname = f"Switch{s+1}_Subnet{idx}"
#             add_device(switch_hostname, switch_ip, role="switch")
#             ip_index += 1
#             topology[subnet_name]["switches"].append({"hostname": switch_hostname, "ip": switch_ip, "devices": []})

#         # --- Add end devices ---
#         for role_name in ["server", "client", "ip_phone"]:
#             count = roles.get(role_name, 0)
#             for c in range(count):
#                 if ip_index >= len(usable_ips):
#                     break
#                 host_ip = usable_ips[ip_index]
#                 hostname = f"{role_name.capitalize()}{c+1}_Subnet{idx}"
#                 add_device(hostname, host_ip, role=role_name)
#                 ip_index += 1
#                 if topology[subnet_name]["switches"]:
#                     switch = random.choice(topology[subnet_name]["switches"])
#                     switch["devices"].append({"hostname": hostname, "ip": host_ip})

#     return topology

# # -----------------------------
# # Step 3: Provision Network Configs
# # -----------------------------
# def provision_network(topology):
#     conn = get_connection()
#     cur = conn.cursor()

#     subnet_networks = {name: data["network"] for name, data in topology.items()}

#     for subnet_name, subnet_data in topology.items():
#         network_cidr = subnet_data["network"]
#         network_ip, prefix = network_cidr.split('/')
#         prefix = int(prefix)

#         router = subnet_data.get("router")
#         switches = subnet_data.get("switches", [])

#         # Router config
#         if router:
#             hostname = router["hostname"]
#             router_ip = router["ip"]
#             config_lines = [
#                 f"hostname {hostname}",
#                 f"interface Gig0/0\n ip address {router_ip} {prefix}\n no shutdown"
#             ]
#             for other_subnet_name, other_network in subnet_networks.items():
#                 if other_subnet_name == subnet_name:
#                     continue
#                 config_lines.append(f"ip route {other_network} {router_ip}")  # placeholder route
#             config_text = "\n".join(config_lines)
#             cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (hostname,))
#             device_id = cur.fetchone()[0]
#             add_config(device_id, config_text)

#         # Switch configs
#         for switch in switches:
#             hostname = switch["hostname"]
#             switch_ip = switch["ip"]
#             config_lines = [
#                 f"hostname {hostname}",
#                 f"interface Vlan1\n ip address {switch_ip} {prefix}\n no shutdown",
#                 "spanning-tree mode rapid-pvst"
#             ]
#             config_text = "\n".join(config_lines)
#             cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (hostname,))
#             device_id = cur.fetchone()[0]
#             add_config(device_id, config_text)

#             # End devices connected to switch
#             for device in switch.get("devices", []):
#                 d_hostname = device["hostname"]
#                 d_ip = device["ip"]
#                 config_text = f"hostname {d_hostname}\nip address {d_ip} {prefix}\n!"
#                 cur.execute("SELECT device_id FROM devices WHERE hostname=%s;", (d_hostname,))
#                 device_id = cur.fetchone()[0]
#                 add_config(device_id, config_text)

#     conn.commit()
#     cur.close()
#     conn.close()
#     print("[✓] Network provisioning complete.")

# # -----------------------------
# # Step 4: Convenience
# # -----------------------------
# def assign_and_provision(subnets, get_usable_ips):
#     topology = generate_topology(subnets, get_usable_ips)
#     provision_network(topology)
#     return topology

# # -----------------------------
# # Step 5: Export Full Configs to Desktop
# # -----------------------------
# def export_full_configs(topology):
#     desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')
#     folder_name = "SNAP_Full_Configs"
#     folder_path = os.path.join(desktop, folder_name)
#     os.makedirs(folder_path, exist_ok=True)

#     for sn, data in topology.items():
#         # JSON
#         json_path = os.path.join(folder_path, f"{sn}_configs.json")
#         json_data = []

#         # TXT
#         txt_path = os.path.join(folder_path, f"{sn}_configs.txt")
#         text_data = ""

#         # Router
#         router = data["router"]
#         if router:
#             json_data.append({
#                 "hostname": router["hostname"],
#                 "ip": router["ip"],
#                 "role": "router"
#             })
#             text_data += f"Hostname: {router['hostname']}\nIP: {router['ip']}\nRole: router\n{'-'*40}\n"

#         # Switches and connected devices
#         for sw in data["switches"]:
#             json_data.append({
#                 "hostname": sw["hostname"],
#                 "ip": sw["ip"],
#                 "role": "switch"
#             })
#             text_data += f"Hostname: {sw['hostname']}\nIP: {sw['ip']}\nRole: switch\n{'-'*40}\n"
#             for device in sw.get("devices", []):
#                 json_data.append({
#                     "hostname": device["hostname"],
#                     "ip": device["ip"],
#                     "role": "end_device"
#                 })
#                 text_data += f"Hostname: {device['hostname']}\nIP: {device['ip']}\nRole: end_device\n{'-'*40}\n"

#         # Save files
#         with open(json_path, "w") as f:
#             json.dump(json_data, f, indent=4)
#         with open(txt_path, "w") as f:
#             f.write(text_data)

#     print(f"[✓] Full configs exported to {folder_path}")

# # -----------------------------
# # Step 6: Main CLI Flow
# # -----------------------------
# if __name__ == "__main__":
#     print("=== SNAP CLI: Technician Mode ===\n")

#     network, num_subnets, hosts_per_subnet = get_network_input()
#     subnets = calculate_subnets(network, num_subnets, hosts_per_subnet)
#     if not subnets:
#         print("[!] No subnets could be calculated. Exiting.")
#         exit(1)

#     from subnet_calc import get_usable_ips
#     print(f"\n[*] Creating topology for {len(subnets)} subnet(s)...")
#     topology = assign_and_provision(subnets, get_usable_ips)

#     print("\n[✓] Topology and configs created successfully.\n")
#     for sn, data in topology.items():
#         print(f"{sn}:")
#         print(f"  Router: {data['router']}")
#         for sw in data['switches']:
#             print(f"  Switch: {sw['hostname']} -> Devices: {[d['hostname'] for d in sw['devices']]}")

#     # Export configs
#     export_full_configs(topology)

