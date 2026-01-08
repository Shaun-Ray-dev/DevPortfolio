import os
import json
from pathlib import Path

# Parse input:
def net_and_mask_input(network):
    net_split = network.split("/")
    net = net_split[0]
    mask = net_split[1]
    mask = int(mask)
    octet_split = net.split(".")
    octet_value = []
    for octet in octet_split:
        octet_value.append(int(octet))
    return octet_value, mask
# Calculate subnet mask:
def mask_value(CIDR_value):
    binary_mask = '1' * CIDR_value + '0' * (32 - CIDR_value)
    oct1 = binary_mask[0:8]
    oct2 = binary_mask[8:16]
    oct3 = binary_mask[16:24]
    oct4 = binary_mask[24:32]
    dec_oct1 = int(oct1, 2)
    dec_oct2 = int(oct2, 2)
    dec_oct3 = int(oct3, 2)
    dec_oct4 = int(oct4, 2)
    return[dec_oct1, dec_oct2, dec_oct3, dec_oct4]
# Calculate wildcard mask:
def wildcard_mask(subnet_mask):
    return [255 - octet for octet in subnet_mask]
# Calculate network address:
def network_address(ip_octets, subnet_mask):
    octet_value = []
    for ip_octet, mask_octet in zip(ip_octets, subnet_mask):
        result_octet = ip_octet & mask_octet
        octet_value.append(result_octet)
    return octet_value
# Calculate broadcast address:
def broadcast_address(ip_octets, subnet_mask):
    broadcast_value = []
    for ip_octet, mask_octet in zip(ip_octets, subnet_mask):
        result_octet = ip_octet | (255 - mask_octet)
        broadcast_value.append(result_octet)
    return broadcast_value
# Calculate first usable host:
def first_usable_host(network_addr, mask):
    if mask >= 31:
        return None
    
    host = network_addr[:]
    host[3] += 1

    for i in range(3, -1, -1):
        if host[i] > 255:
            host[i] = 0
            host[i-1] += 1
    return host
# Calculate last usable host:
def last_usable_host(broadcast_addr, mask):
    if mask >= 31:
        return None
    
    host = broadcast_addr[:]
    host[3] -= 1

    for i in range(3, -1, -1):
        if host[i] < 0:
            host[i] = 255
            host[i-1] -= 1
    return host
# Calculate total hosts:
def total_host(mask):
    if mask == 31:
        return 2
    elif mask == 32:
        return 1
    return 2 ** (32 - mask) - 2
# Validate inputs by user:
def validate_inputs(ip_octets, mask):
    if len(ip_octets) != 4:
        return False
    
    for octet in ip_octets:
        if not (0 <= octet <= 255):
            return False
        
    if not (0 <= mask <= 32):
        return False
    
    return True
# results:
def main():
    all_networks = []

    while True:
        network_input = input("Enter IP address with CIDR (or type 'done' to finish): ")
        if network_input.lower() == "done":
            break

        try:
            ip_octets, mask = net_and_mask_input(network_input)
        except (ValueError, IndexError):
            print("Invalid format used. Please use X.X.X.X/Y")
            continue

        if not validate_inputs(ip_octets, mask):
            print("Invalid IP or subnet mask.")
            continue

        all_networks.append((ip_octets, mask))
        print("Added. Add another or type 'done' to finish.")

    print("\nSubnet info:")
    for ip_octets, mask in all_networks:
        subnet = mask_value(mask)
        net_addr = network_address(ip_octets, subnet)
        bcast_addr = broadcast_address(ip_octets, subnet)
        first_host = first_usable_host(net_addr, mask)
        last_host = last_usable_host(bcast_addr, mask)
        total = total_host(mask)
        wildcard = wildcard_mask(subnet)

        print("\n------------Results---------------")
        print(f"IP Address: {'.'.join(map(str, ip_octets))}")
        print(f"Subnet Mask: {'.'.join(map(str, subnet))}")
        print(f"Wildcard Mask: {'.'.join(map(str, wildcard))}")
        print(f"Network Address: {'.'.join(map(str, net_addr))}")
        print(f"Broadcast Address: {'.'.join(map(str, bcast_addr))}")
        print(f"First Usable Host: {'.'.join(map(str, first_host)) if first_host else 'N/A'}")
        print(f"Last Usable Host: {'.'.join(map(str, last_host)) if last_host else 'N/A'}")
        print(f"Total Hosts: {total}")
        
# ---------------- Save to Desktop folder ----------------

    desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')
    folder_name = "Subnet_Calculations"
    folder_path = os.path.join(desktop, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    print(f"Folder will be created at: {folder_path}")

    results_text = ""
    results_json = []

    for ip_octets, mask in all_networks:
        subnet = mask_value(mask)
        net_addr = network_address(ip_octets, subnet)
        bcast_addr = broadcast_address(ip_octets, subnet)
        first_host = first_usable_host(net_addr, mask)
        last_host = last_usable_host(bcast_addr, mask)
        total = total_host(mask)
        wildcard = wildcard_mask(subnet)

# Text version
        results_text += f"\nIP Address: {'.'.join(map(str, ip_octets))}\n"
        results_text += f"Subnet Mask: {'.'.join(map(str, subnet))}\n"
        results_text += f"Wildcard Mask: {'.'.join(map(str, wildcard))}\n"
        results_text += f"Network Address: {'.'.join(map(str, net_addr))}\n"
        results_text += f"Broadcast Address: {'.'.join(map(str, bcast_addr))}\n"
        results_text += f"First Usable Host: {'.'.join(map(str, first_host)) if first_host else 'N/A'}\n"
        results_text += f"Last Usable Host: {'.'.join(map(str, last_host)) if last_host else 'N/A'}\n"
        results_text += f"Total Hosts: {total}\n"
        results_text += "--------------------------------\n"

# JSON version
        results_json.append({
            "IP Address": '.'.join(map(str, ip_octets)),
            "Subnet Mask": '.'.join(map(str, subnet)),
            "Wildcard Mask": '.'.join(map(str, wildcard)),
            "Network Address": '.'.join(map(str, net_addr)),
            "Broadcast Address": '.'.join(map(str, bcast_addr)),
            "First Usable Host": '.'.join(map(str, first_host)) if first_host else None,
            "Last Usable Host": '.'.join(map(str, last_host)) if last_host else None,
            "Total Hosts": total
        })

    with open(os.path.join(folder_path, "subnet_results.txt"), "w") as txt_file:
        txt_file.write(results_text)

    with open(os.path.join(folder_path, "subnet_results.json"), "w") as json_file:
        json.dump(results_json, json_file, indent=4)

    print(f"\nResults saved to folder: {folder_path}")


if __name__ == "__main__":
    main()