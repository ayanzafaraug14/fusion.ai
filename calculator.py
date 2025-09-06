# Get input from the user (or from your AI)
first_number = int(input("Enter first number: "))
operator = input("Enter operator (+, -, *, /, %, //, **): ")
second_number = int(input("Enter second number: "))

# Perform operation based on the operator
if operator == "+":
    print(first_number + second_number)
elif operator == "-":
    print(first_number - second_number)
elif operator == "*":
    print(first_number * second_number)
elif operator == "/":
    if second_number != 0:
        print(first_number / second_number)
    else:
        print("Error: Division by zero")
elif operator == "%":
    if second_number != 0:
        print(first_number % second_number)
    else:
        print("Error: Division by zero")
elif operator == "//":
    if second_number != 0:
        print(first_number // second_number)
    else:
        print("Error: Division by zero")
elif operator == "**":
    print(first_number ** second_number)
else:
    print("Invalid operator")
