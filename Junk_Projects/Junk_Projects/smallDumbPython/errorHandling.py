### **41–45: Simple Error Handling (Try/Except)**

# 41. Ask for a number and divide 100 by it; handle division by zero.

# try:
#     num = int(input("Enter any number: "))
#     result = 100 / num
#     print(f"100 divided by {num} is {result}")
# except ZeroDivisionError:
#     print("Error: Cannot divide by zero.")
# except ValueError:
#     print("Error: Please enter valid number.")

# 42. Open a file that may not exist, handle “file not found.”

# try:
#     filename = input("Enter a filename to open: ")
#     with open(filename, "r") as file:
#         content = file.read()
#         print("File content:")
# except FileNotFoundError:
#     print(f"Error: The file '{filename}' does not exist.")

# 43. Convert user input to an integer; handle invalid input gracefully.

# try: 
#     user_input = input("Enter a number: ")
#     number = int(user_input)
#     print(f"You entered the number {number}")
# except ValueError:
#     print(f"Error: '{user_input}' is not a valid number.")

# 44. Read a file and catch any unexpected errors, printing “Something went wrong.”

# filename = input("Enter the filename to open: ")

# try:
#     with open(filename, "r") as file:
#         content = file.read()
#         print("File content:")
#         print(content)
# except Exception:
#     print("Something went wrong.")

# 45. Try accessing an index in a list; handle index out-of-range errors.

# my_list = [10, 20, 30, 40, 50]

# try:
#     index = int(input("Enter the index you want to access: "))
#     value = my_list[index]
#     print(f"Value at index {index} is {value}")
# except IndexError:
#     print(f"Error: Index {index} is out of range. Valid indexes are 0 to {len(my_list)-1}.")
# except ValueError:
#     print("Error: Please enter a valid integer index.")







