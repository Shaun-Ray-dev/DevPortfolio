### **36–40: File I/O Basics**

# 36. Create a text file and write your name in it.

# with open("name.txt", "w") as file:
#     file.write("Shaun")

# 37. Read a file and print only lines containing the word “error.”

# with open("log.txt", "r") as file:
#     for line in file:
#         if "error" in line.lower():
#             print(line.strip())

# or

# count = 0
# with open("log.txt", "r") as file:
#     for line in file:
#         if "error" in line.lower():
#             count += 1

# print(f"Total errors: {count}")

# 38. Append a new line with today’s date to a file.

# from datetime import date

# with open("dates.txt", "a") as file:
#     file.write(f"{date.today()}\n")

# 39. Count the number of lines in a file.

# count = 0

# with open("log.txt", "r") as file:
#     for _ in file:
#         count += 1

# print(f"Number of lines: {count}")

# 40. Copy contents of one file into a new file.

# with open("log.txt", "r") as src:
#     with open("copy.txt", "w") as dest:
#         for line in src:
#             dest.write(line)

