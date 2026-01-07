import os
import platform
import psutil

def collect_system_info():
    info = {
        "hostname": platform.node(),
        "os": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent
    }
    return info

if __name__=="__main__":
    data = collect_system_info()
    print(data)