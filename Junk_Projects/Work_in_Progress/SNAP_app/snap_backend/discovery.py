# # snap_backend/discovery.py
# """
# SNAP discovery — simple, reliable POC.
# Uses python-nmap but forces the scanner to the full nmap.exe path so PATH isn't required.
# Returns list of dicts: {'ip','hostname','mac','vendor'}.
# """

# import nmap

# # <-- Set to the full path you found. No PATH edits required.
# NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"

# def scan_subnet(subnet_cidr, ping_only=True):
#     """
#     Scan a subnet and return discovered hosts.
#     Args:
#         subnet_cidr (str): e.g. "172.25.64.0/24" or "172.25.64.0/20"
#         ping_only (bool): if True uses -sn (faster, safer). If False, you can change args for more detail.
#     Returns:
#         List[dict]
#     """
#     nm = nmap.PortScanner(nmap_search_path=(NMAP_PATH,))
#     devices = []
#     arguments = '-sn' if ping_only else ''

#     try:
#         print(f"[discovery] starting scan {subnet_cidr} (args: '{arguments}')")
#         nm.scan(hosts=subnet_cidr, arguments=arguments)

#         for host in nm.all_hosts():
#             info = nm[host]
#             # safe access patterns: nm returns nested dicts
#             hostname = info.get('hostnames')[0]['name'] if info.get('hostnames') else None
#             addrs = info.get('addresses', {})
#             mac = addrs.get('mac') if isinstance(addrs, dict) else None
#             vendor = info.get('vendor') if isinstance(info, dict) and info.get('vendor') else None

#             device = {
#                 "ip": host,
#                 "hostname": hostname,
#                 "mac": mac,
#                 "vendor": vendor
#             }
#             devices.append(device)

#         print(f"[discovery] scan complete. {len(devices)} hosts found.")
#         return devices

#     except Exception as e:
#         print(f"[discovery] error during scan: {e}")
#         return []
