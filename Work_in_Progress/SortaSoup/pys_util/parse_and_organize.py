import os
import shutil
import json
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPED_DIR = os.path.join(BASE_DIR, "..", "scraped_files")
PROC_HTML_DIR = os.path.join(BASE_DIR, "..", "proc_html")
SORTED_DIR = os.path.join(BASE_DIR, "..", "sorted_files")

for folder in ["Images", "Text", "JSON", "HTML"]:
    os.makedirs(os.path.join(SORTED_DIR, folder), exist_ok=True)

for file in os.listdir(PROC_HTML_DIR):
    path = os.path.join(PROC_HTML_DIR, file)

    if file.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        data = {"content": lines}

        json_file = os.path.join(SORTED_DIR, "JSON", file.replace(".txt", ".json"))
        with open(json_file, "w", encoding="utf-8") as j:
            json.dump(data, j, indent=2)

        shutil.copy(path, os.path.join(SORTED_DIR, "Text", file))


for file in os.listdir(SCRAPED_DIR):
    src = os.path.join(SCRAPED_DIR, file)
    if file.endswith(".html"):
        shutil.copy(src, os.path.join(SORTED_DIR, "HTML", file))
    elif file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        shutil.copy(src, os.path.join(SORTED_DIR, "Images", file))

for json_file in os.listdir(os.path.join(SORTED_DIR, "JSON")):
    json_path = os.path.join(SORTED_DIR, "JSON", json_file)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html_file = os.path.join(SORTED_DIR, "HTML", json_file.replace(".json", ".html"))
    if os.path.exists(html_file):
        soup = BeautifulSoup(open(html_file, encoding="utf-8"), "html.parser")
        data["links"] = [a.get("href") for a in soup.find_all("a")]
        data["images"] = [img.get("src") for img in soup.find_all("img")]
        data["title"] = soup.title.string if soup.title else None

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

print("SortaSoup processing complete.")
