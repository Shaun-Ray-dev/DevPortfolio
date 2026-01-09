import subprocess
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(LOG_DIR, f"run_{timestamp}.log")
report_file = os.path.join(REPORT_DIR, f"summary_{timestamp}.txt")

def run_command(command, shell=False):
    with open(log_file, "a") as log:
        log.write(f"\n--- Running: {command} ---\n")
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                check=True
            )
            log.write(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            log.write(e.stderr)
            return f"ERROR: {e.stderr}"

def main():
    summary = []

    summary.append("SYSTEMOPS AUTOMATION SUMMARY")
    summary.append(f"Run Time: {datetime.now()}\n")

    summary.append("1. Local System Metrics")
    summary.append(run_command([sys.executable, os.path.join(SRC_DIR, "system_monitor.py")]))

    summary.append("\n2. Network Scan")
    summary.append(run_command([sys.executable, os.path.join(SRC_DIR, "network_scanner.py")]))

    summary.append("\n3. Remote Metrics")
    summary.append(run_command([sys.executable, os.path.join(SRC_DIR, "remote_metrics.py")]))

    summary.append("\n4. Compliance Check")
    summary.append(run_command([sys.executable, os.path.join(SRC_DIR, "compliance_check.py")]))

    if os.name == "nt":
        summary.append("\n5. Windows Config Backup")
        summary.append(run_command(
            ["powershell", "-ExecutionPolicy", "Bypass",
             "-File", os.path.join(SRC_DIR, "backup_config.ps1")],
            shell=False
        ))
    else:
        summary.append("\n5. Linux Health Check")
        summary.append(run_command(
            ["bash", os.path.join(SRC_DIR, "check_health.sh")]
        ))

    with open(report_file, "w") as report:
        report.write("\n".join(summary))

    print(f"\n✔ Automation complete")
    print(f"✔ Log file: {log_file}")
    print(f"✔ Report file: {report_file}")

if __name__ == "__main__":
    main()
