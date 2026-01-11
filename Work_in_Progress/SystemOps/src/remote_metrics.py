def get_remote_metrics(host, username, password):
    return {
        "host": host,
        "uptime": "5 days, 4:32",
        "cpu_percent": 23.5,
        "ram_percent": 48.2,
        "disk_percent": 62.1
    }

if __name__ == "__main__":
    demo_hosts = ["192.168.1.100", "192.168.1.101"]

    for host in demo_hosts:
        data = get_remote_metrics(host, "user", "pass")
        print(data)