"""
vault.py
Secure storage and retrieval of credentials for SNAP project.
Uses environment variables by default, with optional Fernet encryption.
"""

import os
from cryptography.fernet import Fernet, InvalidToken

# ---------------------------
# Optional: Fernet Encryption
# ---------------------------
FERNET_KEY = os.environ.get("SNAP_VAULT_KEY")
fernet = None
if FERNET_KEY:
    try:
        fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)
    except Exception as e:
        print(f"[!] Invalid FERNET_KEY, encryption disabled: {e}")
        fernet = None

# ---------------------------
# Save credentials
# ---------------------------
def save_credential(name: str, value: str):
    """
    Save credential to environment (for dev) or encrypted form (optional)
    """
    if fernet:
        token = fernet.encrypt(value.encode()).decode()
        os.environ[name] = token
    else:
        os.environ[name] = value

# ---------------------------
# Retrieve credentials
# ---------------------------
def get_credential(name: str) -> str:
    """
    Retrieve credential from environment (or decrypt if using Fernet)
    """
    value = os.environ.get(name)
    if not value:
        raise KeyError(f"Credential '{name}' not found in environment")
    if fernet:
        try:
            return fernet.decrypt(value.encode()).decode()
        except InvalidToken:
            raise ValueError(f"[!] Invalid encrypted credential for '{name}'")
    return value

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    # Save a test credential
    save_credential("SNAP_TEST_PASSWORD", "supersecret123")

    # Retrieve it
    pwd = get_credential("SNAP_TEST_PASSWORD")
    print("Retrieved:", pwd)





# import os
# from cryptography.fernet import Fernet

# # ---------------------------
# # Optional: AES Encryption
# # ---------------------------
# # Only use if you want to encrypt credentials on disk
# # Generate a key once and store in an env var or secure file
# # Example to generate a key: Fernet.generate_key()
# FERNET_KEY = os.environ.get("SNAP_VAULT_KEY")
# fernet = Fernet(FERNET_KEY) if FERNET_KEY else None

# # ---------------------------
# # Save credentials
# # ---------------------------
# def save_credential(name: str, value: str):
#     """
#     Save credential to environment (for dev) or encrypted file (optional)
#     """
#     if fernet:
#         token = fernet.encrypt(value.encode()).decode()
#         os.environ[name] = token
#     else:
#         os.environ[name] = value


# # ---------------------------
# # Retrieve credentials
# # ---------------------------
# def get_credential(name: str) -> str:
#     """
#     Retrieve credential from environment (or decrypt if using fernet)
#     """
#     value = os.environ.get(name)
#     if not value:
#         raise KeyError(f"Credential '{name}' not found in environment")
#     if fernet:
#         return fernet.decrypt(value.encode()).decode()
#     return value


# # ---------------------------
# # Example usage
# # ---------------------------
# if __name__ == "__main__":
#     # Save a test credential
#     save_credential("SNAP_TEST_PASSWORD", "supersecret123")

#     # Retrieve it
#     pwd = get_credential("SNAP_TEST_PASSWORD")
#     print("Retrieved:", pwd)


