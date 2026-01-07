import subprocess                 
import ipaddress    

def ping_ip(ip):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "200", str(ip)],  
        stdout=subprocess.DEVNULL,                
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0              

def scan_network(subnet):
    active_hosts = []                         

    for ip in ipaddress.IPv4Network(subnet):
        print(f"Pinging {ip}...")                
        if ping_ip(ip):                           
            print(f"  ✔ Host up: {ip}")
            active_hosts.append(str(ip))        

    return active_hosts                            

if __name__ == "__main__":
    subnet = "192.168.1.0/24"                     
    hosts = scan_network(subnet)                  
    print("\nActive hosts found:")
    print(hosts)
