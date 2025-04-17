import os
import platform


class Math:
    def add(self, number_one, number_two):
        return number_one + number_two

    def subtract(self, number_one, number_two):
        return number_two - number_one

    def multiply(self, number_one, number_two):
        return number_one * number_two

    def divide(self, number_one, number_two):
        return number_two / number_one

    def expo(self, number_one, number_two):
        return number_one ** number_two


calc = Math()

while True:
    print("Welcome to the calculator!")
    print("\nType 'exit' at any time to quit.")

    first_input = input('Type first number: ')
    if first_input.lower() == 'exit':
        break

    second_input = input('Type second number: ')
    if second_input.lower() == 'exit':
        break

    operation = input('Please pick the operation (+, -, *, /, **): ')
    if operation.lower() == 'exit':
        break

    # Convert inputs to float
    try:
        number_one = float(first_input)
        number_two = float(second_input)
    except ValueError:
        print('Invalid number. Try again.')
        continue

    # Do the math
    if operation == '+':
        print("Result:", calc.add(number_one, number_two))
    elif operation == '-':
        print("Result:", calc.subtract(number_one, number_two))
    elif operation == '*':
        print("Result:", calc.multiply(number_one, number_two))
    elif operation == '/':
        try:
            print("Result:", calc.divide(number_one, number_two))
        except ZeroDivisionError:
            print("Cannot divide by zero.")
    elif operation == '**':
        print("Result:", calc.expo(number_one, number_two))
    else:
        print("Invalid operation. Try again.")

