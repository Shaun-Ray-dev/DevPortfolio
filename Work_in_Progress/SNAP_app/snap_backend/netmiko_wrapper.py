"""
netmiko_wrapper.py
Wrapper functions for connecting to network devices using Netmiko.
Handles:
- Connect / disconnect
- Run commands
- Backup current config
- Push config changes
"""

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging

# Optional: logging for debugging
logging.basicConfig(level=logging.INFO, format='[netmiko_wrapper] %(message)s')


def connect_device(device_info):
    """
    Connects to a network device using Netmiko.
    device_info: dict containing keys:
        - device_type: 'cisco_ios', 'juniper', etc.
        - host: IP address or hostname
        - username
        - password
        - optional: secret (for enable)
    Returns a Netmiko connection object or None on failure.
    """
    try:
        conn = ConnectHandler(**device_info)
        # Enter enable mode if secret provided
        if 'secret' in device_info and device_info['secret']:
            conn.enable()
        logging.info(f"Connected to {device_info['host']}")
        return conn
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logging.error(f"Failed to connect to {device_info['host']}: {e}")
        return None


def disconnect_device(conn):
    """Safely disconnect a Netmiko connection."""
    if conn:
        conn.disconnect()
        logging.info("Disconnected.")


def run_command(conn, command):
    """
    Run a single command on the device.
    Returns output as string or None on failure.
    """
    if not conn:
        return None
    try:
        output = conn.send_command(command)
        logging.info(f"Ran command on {conn.host}: {command}")
        return output
    except Exception as e:
        logging.error(f"Command failed on {conn.host}: {e}")
        return None


def backup_config(conn):
    """
    Pull the running configuration from the device.
    Returns the config as string or None on failure.
    """
    logging.info(f"Backing up config from {conn.host}...")
    return run_command(conn, "show running-config")


def push_config(conn, commands, dry_run=True):
    """
    Push a list of config commands to the device.
    dry_run=True: only log what would be sent.
    Returns True if successful, False otherwise.
    """
    if not conn:
        return False

    if dry_run:
        logging.info(f"[DRY RUN] Would push to {conn.host}: {commands}")
        return True

    try:
        output = conn.send_config_set(commands)
        logging.info(f"Pushed config to {conn.host}:\n{output}")
        return True
    except Exception as e:
        logging.error(f"Failed to push config to {conn.host}: {e}")
        return False


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_device = {
        "device_type": "cisco_ios",
        "host": "172.25.64.1",
        "username": "admin",
        "password": "password",
        "secret": "enablepassword",
    }

    conn = connect_device(test_device)
    if conn:
        config = backup_config(conn)
        print(config)
        push_config(conn, ["hostname TestDevice"], dry_run=True)
        disconnect_device(conn)
