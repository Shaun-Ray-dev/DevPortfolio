import os
import shutil

folder_path = "test_files"

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".log", ".md", ".csv"],
    "Python": [".py"],
    "PowerShell": [".ps1"],
    "Bash": [".sh"],
    "JavaScript": [".js"],
    "Others": []
}

for folder in file_types:
    folder_dir = os.path.join(folder_path, folder)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

for filename in os.listdir(folder_path):
    if filename.startswith("."):  
        continue

    file_path = os.path.join(folder_path, filename)
    if os.path.isdir(file_path):
        continue

    moved = False
    for folder, extensions in file_types.items():
        if any(filename.lower().endswith(ext) for ext in extensions):
            shutil.move(file_path, os.path.join(folder_path, folder, filename))
            moved = True
            break

    if not moved:
        shutil.move(file_path, os.path.join(folder_path, "Others", filename))

print("Files organized successfully!")
