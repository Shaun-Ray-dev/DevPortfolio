import paramiko

def get_remote_metrics(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command("uptime")
    uptime = stdout.read().decode().strip()

    stdin, stdout, stderr = ssh.exec_command(
        "free -m | awk 'NR==2{printf \"%s\", $3/$2*100 }'"
    )
    ram_percent = stdout.read().decode().strip()

    ssh.close()

    return {"host": host, "uptime": uptime, "ram_percent": ram_percent}

if __name__ == "__main__":
    host = "192.168.1.100"
    username = "user"
    password = "pass"
    data = get_remote_metrics(host, username, password)
    print(data)