### **46–50: Data Structures Beyond Lists**

# 46. Create a dictionary of 3 items, update one value, and print the dictionary.

# my_dict = {
#     "name": "Shaun",
#     "age": "39",
#     "city": "Wilkesboro"
# }

# my_dict["age"] = 40

# print(my_dict)

# 47. Count how many times each letter appears in a string using a dictionary.

# text = "Hey yall"

# letter_count = {}

# for char in text:
#     if char != " ":
#         if char in letter_count:
#             letter_count[char] += 1
#         else:
#             letter_count[char] = 1

# print(letter_count)

# 48. Remove a key from a dictionary safely.

# my_dict = {"name": "Shaun", "age": 39, "city": "Wilkesboro"}

# removed_value = my_dict.pop("age", None)

# print(my_dict)
# print("Removed value:", removed_value)

# 49. Create a list of dictionaries representing 3 people with name and age; print each person’s age.

# people = [
#     {"name": "Shaun", "age": 39},
#     {"name": "Becca", "age": 29},
#     {"name": "Elizabeth", "age": 27}
# ]

# for person in people:
#     print(person["age"])

# 50. Merge two dictionaries into one and print the result.

# dict_1 = {"name": "Shaun", "age": 39}
# dict_2 = {"city": "Wilkesboro", "Job": "Engineer"}

# merge_dict = dict_1 | dict_2

# print(merge_dict)

