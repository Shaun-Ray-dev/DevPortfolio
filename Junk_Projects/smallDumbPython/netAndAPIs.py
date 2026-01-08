### **56–60: Networking & APIs**

# 56. Ping a single IP address and print if it’s reachable.

# import subprocess

# ip = input("Please enter an IP address to ping: ")

# result = subprocess.run(["ping", "-n", "1", ip], capture_output=True)

# if result.returncode == 0:
#     print(f"{ip} is reachable.")
# else:
#     print(f"{ip} is NOT reachable.")

# 57. Fetch data from `https://api.github.com` and print the response.

# import requests
# import json

# url = "https://api.github.com"

# response = requests.get(url)
# data = response.json()

# with open("github_api.json", "w") as file:
#     json.dump(data, file, indent=4)

# print("Data saved to github_api.json")

# or

# import requests
# import json

# url = input("Enter a URL to fetch JSON from: ")

# try:
#     response = requests.get(url)
#     response.raise_for_status()

#     try:
#         data = response.json()
#         with open("output.json", "w") as file:
#             json.dump(data, file, indent=4)
#         print("JSON data saved to output.json")
#     except ValueError:
#         print("The site did not return JSON")

# except requests.RequestException as e:
#     print(f"Error fetching the URL: {e}")

# 58. Print your computer’s local IP address.

# import socket

# hostname = socket.gethostname()
# local_ip = socket.gethostbyname(hostname)

# print(f"Your local IP address is: {local_ip}")

# 59. Check if a website is online using `requests.get()`.

# import requests

# url = input("Enter a website url to check: ")

# try:
#     response = requests.get(url, timeout=5)
#     if response.status_code == 200:
#         print(f"{url} is online.")
#     else:
#         print(f"{url} responded with status code of {response.status_code}")
# except requests.RequestException:
#     print(f"{url} is offline or unreachable.")

# 60. Parse JSON from an API and print a single field.

# import requests

# url = "https://api.github.com"

# response = requests.get(url)
# data = response.json()

# print("Current user URL:", data["current_user_url"])







