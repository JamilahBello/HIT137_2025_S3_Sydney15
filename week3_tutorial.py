# code to calculate the sum of even and odd numbers entered by the user

# sett up initial sums
sum_even = 0
sum_odd = 0

# loop to get user input
while True:
    user_input = input("Enter a number ")

    # break the loop if input is empty
    if user_input == "":
        break

    if not user_input.isdigit() and  not user_input.lstrip("-").isdigit() and not (user_input.find(".") == -1 and user_input.replace(".", "", 1).lstrip("-").isdigit()):
        print("Please enter a valid number.")
        continue

    number = int(user_input)

    # check if the number is even or odd
    if number % 2 == 0:
        sum_even += number
    else:
        sum_odd += number

# print the results
print(f"Sum of even number: {sum_even}")
print(f"Sum of Odd number: {sum_odd}")


# second question
