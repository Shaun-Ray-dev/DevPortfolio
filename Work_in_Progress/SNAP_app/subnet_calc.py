import os
import json
import ipaddress

# --- Get usable IPs in a subnet ---
def get_usable_ips(network_ip, mask):
    """
    Returns a list of usable host IPs in a subnet using ipaddress module.
    Automatically handles /31 and /32 correctly.
    """
    try:
        net = ipaddress.ip_network(f"{network_ip}/{mask}", strict=False)
        return [str(ip) for ip in net.hosts()]
    except ValueError as e:
        print(f"[!] Invalid network: {network_ip}/{mask} ({e})")
        return []

# --- Generate subnet report ---
def report_subnets(subnets, folder_name="Subnet_Calculations"):
    """
    Generates a text and JSON report for given IPv4Network objects.
    Saves to Desktop\folder_name.
    """
    desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')
    folder_path = os.path.join(desktop, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    results_text = ""
    results_json = []

    for subnet in subnets:
        if not isinstance(subnet, ipaddress.IPv4Network):
            print(f"[!] Skipping invalid subnet: {subnet}")
            continue

        subnet_mask = str(subnet.netmask)
        wildcard_mask = str(subnet.hostmask)
        network_address = str(subnet.network_address)
        broadcast_address = str(subnet.broadcast_address)
        usable_ips = list(subnet.hosts())
        first_host = str(usable_ips[0]) if usable_ips else None
        last_host = str(usable_ips[-1]) if usable_ips else None
        total = len(usable_ips)

        results_text += f"\nNetwork: {subnet}\n"
        results_text += f"Subnet Mask: {subnet_mask}\n"
        results_text += f"Wildcard Mask: {wildcard_mask}\n"
        results_text += f"Network Address: {network_address}\n"
        results_text += f"Broadcast Address: {broadcast_address}\n"
        results_text += f"First Host: {first_host if first_host else 'N/A'}\n"
        results_text += f"Last Host: {last_host if last_host else 'N/A'}\n"
        results_text += f"Total Hosts: {total}\n--------------------------------\n"

        results_json.append({
            "Network": str(subnet),
            "Subnet Mask": subnet_mask,
            "Wildcard Mask": wildcard_mask,
            "Network Address": network_address,
            "Broadcast Address": broadcast_address,
            "First Host": first_host,
            "Last Host": last_host,
            "Total Hosts": total
        })

    with open(os.path.join(folder_path, "subnet_results.txt"), "w") as f:
        f.write(results_text)
    with open(os.path.join(folder_path, "subnet_results.json"), "w") as f:
        json.dump(results_json, f, indent=4)

    print(f"[✓] Subnet report saved to {folder_path}")

# --- Optional: quick test ---
if __name__ == "__main__":
    import ipaddress
    test_subnets = [
        ipaddress.IPv4Network("192.168.10.0/28"),
        ipaddress.IPv4Network("192.168.20.0/29")
    ]
    report_subnets(test_subnets)

