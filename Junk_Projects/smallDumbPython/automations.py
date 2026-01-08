### **51–55: File & Folder Automation (Prep Exercises)**

# 51. Print a list of all files in a folder.

# from pathlib import Path

# folder_path = Path(r"C:\Users\shaun\OneDrive\Desktop\smallDumbPython")

# for item in folder_path.iterdir():
#     print(item.name)

# 52. Ask the user for a folder name and check if it exists.

# from pathlib import Path

# folder_name = input("Please enter a folder path: ")

# folder = Path(folder_name)

# if folder.exists() and folder.is_dir():
#     print("Folder exists.")
# else:
#     print("Folder does NOT exists.")

# 53. Create a new folder called `TestFolder`.

# from pathlib import Path

# new_folder = Path("TestFolder")

# new_folder.mkdir(exist_ok=True)

# print("TestFolder created (or already exist)")

# or

# from pathlib import Path

# base_path = Path(r"C:\Users\shaun\OneDrive\Desktop\smallDumbPython")
# new_folder = base_path / "TestFolder"

# new_folder.mkdir(exist_ok=True)

# print("TestFolder created inside smallDumbPython.")

# 54. Rename a single file in a folder.

# from pathlib import Path

# folder = Path(r"C:\Users\shaun\OneDrive\Desktop\smallDumbPython")

# old_name = input("Enter the current filename: ")
# new_name = input("Enter the new filename: ")

# old_file = folder / old_name
# new_file = folder / new_name

# if old_file.exists():
#     old_file.rename(new_file)
#     print("File renamed.")
# else:
#     print("File does not exist.")

# 55. Move one file from one folder to another.

# from pathlib import Path

# source = Path(input("Enter source folder path: "))
# destination = Path(input("Enter destination folder path: "))
# file_name = input("Enter filename to move: ")

# source_file = source / file_name
# dest_file = destination / file_name

# if source_file.exists():
#     destination.mkdir(exist_ok=True)
#     source_file.rename(dest_file)
#     print("File moved.")
# else:
#     print("File not found.")

