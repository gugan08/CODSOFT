import sys # Imported for a clean exit, giving it a manually added touch

# --- Core Arithmetic Functions ---

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero. Please try a different number.")
    return a / b

def power_numbers(a, b):
    return a ** b

# --- Operation Dispatcher ---
# Maps symbols to functions, avoiding a long chain of if/elif statements
OPERATION_MAP = {
    '+': add_numbers,
    '-': subtract_numbers,
    '*': multiply_numbers,
    '/': divide_numbers,
    '**': power_numbers, # Added a bonus operation for uniqueness!
}

# --- Main Logic ---

def run_calculator():
    print("\n=== Advanced Simple Calculator ===")
    print("Available Operations: +, -, *, /, ** (Power)")
    print("Type 'exit' or 'quit' at any time to stop.")

    while True:
        # Get first number with error handling
        try:
            input_a = input("Enter the first number (A): ").strip()
            if input_a.lower() in ('exit', 'quit'):
                sys.exit(0)
            number_a = float(input_a)
        except ValueError:
            print("Invalid input for the first number. Please enter a valid numerical value.")
            continue # Go back to the start of the loop

        # Get operation choice
        operation = input("Enter the operation symbol (+, -, *, /, **): ").strip()
        if operation.lower() in ('exit', 'quit'):
            sys.exit(0)
        if operation not in OPERATION_MAP:
            print(f"'{operation}' is not a recognized operation. Please try again.")
            continue

        # Get second number with error handling
        try:
            input_b = input("Enter the second number (B): ").strip()
            if input_b.lower() in ('exit', 'quit'):
                sys.exit(0)
            number_b = float(input_b)
        except ValueError:
            print("Invalid input for the second number. Please enter a valid numerical value.")
            continue # Go back to the start of the loop

        # Perform the calculation
        try:
            # Retrieve the function from the map and call it with the numbers
            calculation_function = OPERATION_MAP[operation]
            result = calculation_function(number_a, number_b)

            # Display the result formatted
            print(f"Result:")
            print(f"   {number_a} {operation} {number_b} = {result}")

        except ZeroDivisionError as e:
            print(f"Calculation Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Entry point
if __name__ == "__main__":
    try:
        run_calculator()
    except SystemExit:
        print("\nCalculator closed. Thank you for using it!")