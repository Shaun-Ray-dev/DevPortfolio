import psutil
import platform

def collect_system_info():
    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('C:\\').percent 
    }
    