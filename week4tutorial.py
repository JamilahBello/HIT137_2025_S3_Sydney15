# smallerst number
numbers = [45, 23, 89, 12, 56, 34]
print(f"Smallest number: {min(numbers)}")



# script to concatenate several dictionaries into one
dic1 = {1:10, 2:20}
dic2 = {3:30, 4:40}
dic3 = {5:50, 6:60}
dic4 = {**dic1, **dic2, **dic3}
print(f"Concatenated dictionary: {dic4}")

# question three
# Assume that the variable data refers to the dictionary {“b”:20, “a”:35}. Write the
# expressions that perform the following tasks:
# a. Replace the value at the key “b” in data with that value’s negation.
# b. Add the key/value pair “c”:40 to data.
# c. Remove the value at key “b” in data, safely.
# d. Print the keys in data in alphabetical order

data = {"b":20, "a":35}
# a. Replace the value at the key “b” in data with that value’s negation.
data["b"] = -data["b"]
# b. Add the key/value pair “c”:40 to data.
data["c"] = 40
# c. Remove the value at key “b” in data, safely.
data.pop("b", None)
# d. Print the keys in data in alphabetical order
for key in sorted(data.keys()):
    print(key)


# Define a function named sum. This function expects two numbers, named low and high, as
# arguments. The function computes and returns the sum of all of the numbers between low
# and high, inclusive
def sum(low, high):
    total = 0
    for num in range(low, high + 1):
        total += num
    return total
