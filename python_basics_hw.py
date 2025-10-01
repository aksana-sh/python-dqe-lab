# Python basics HW
# Create a python script:
# - create list of 100 random numbers from 0 to 1000
# - sort list from min to max (without using sort())
# - calculate average for even and odd numbers, print both average result in console


# Import the random module to generate random numbers
import random


# Step 1: Generate a list of 100 random numbers from 0 to 1000
def gen_random_numbers() -> list:
    """
    Generates a list of 100 random integers between 0 and 1000.

    Returns:
        list: A list containing 100 randomly generated integers.
    """
    # The next code creates a list of 100 random integers using list comprehension
    # 'random.randint(0, 1000)' generates a random integer between 0 and 1000
    # 'range(100)' creates a sequence of 100 iterations (from 0 to 99)
    # 'for n in range(100)' iterates 100 times, generating one random number per iteration
    random_numbers = [random.randint(0, 1000) for _ in range(100)]
    return random_numbers


# Step 2: Sort the list from minimum to maximum without using sort()
def sort_numbers_asc(numbers: list) -> list:
    """
    Sorts a list of numbers in ascending order without modifying the original list.

    Args:
        numbers (list): A list of numeric values.

    Returns:
        list: A new list containing the same numbers sorted from min to max.
    """

    # The next line uses built-in sorted() function to sort the list
    # sorted() returns a new arranged in ascending order list and does not change the original list
    sorted_numbers = sorted(numbers)
    return sorted_numbers


# I wasn't sure if we are allowed to use built-in sorted() method
# Alternative solution
def sort_numbers_asc2(numbers: list) -> list:
    """
    Sorts a list of numbers in ascending order

    Args:
        numbers (list): A list of numeric values to be sorted.

    Returns:
        list: A new list sorted in ascending order.
    """

    # Create a copy of the input list to avoid modifying it
    unsorted_numbers = numbers.copy()

    # Create an empty list to store sorted elements
    sorted_numbers = []

    # Loop until all elements are moved from unsorted to sorted_list
    while unsorted_numbers:
        # Assume the first element is the minimum
        min_value = unsorted_numbers[0]

        # Iterate through the unsorted list to compare min_value with each element to find the actual minimum value
        for num in unsorted_numbers:
            if num < min_value:
                min_value = num

        # Append the smallest value to the sorted list
        sorted_numbers.append(min_value)

        # Remove the smallest value from the unsorted list
        unsorted_numbers.remove(min_value)

    return sorted_numbers


# Step 3: Calculate average for even and odd numbers, print both average result in console
def calculate_average(numbers: list) -> str:
    """
    Calculates and prints the average of even and odd numbers from a given list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        str: A message summarizing the average values.
    """

    # Create a list of even numbers (if a number is divisible by 2 without remainder)
    even_numbers = [num for num in numbers if num % 2 == 0]

    # Create a list of odd numbers (if a number is not divisible by 2 without remainder)
    odd_numbers = [num for num in numbers if num % 2 != 0]

    # Calculate the average values, handle division by zero
    # len() gives the count of numbers
    average_even = sum(even_numbers) / len(even_numbers) if even_numbers else 0
    average_odd = sum(odd_numbers) / len(odd_numbers) if odd_numbers else 0

    # Print the average results
    print(f"Average of even numbers: {average_even}")
    print(f"Average of odd numbers: {average_odd}")

    # Return a formatted summary string
    return f"Even Avg: {average_even}, Odd Avg: {average_odd}"

#  Check input - output
# numbers = gen_random_numbers()
# print(numbers)
#
# numbers_asc = sort_numbers_asc2(numbers)
# print(numbers_asc)
#
# calculate_average(numbers)
# calculate_average(numbers_asc)
