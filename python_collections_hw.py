# Python Collections HW
# Write a code, which will:
# 1. create a list of random number of dicts (from 2 to 10)
# - dict's random numbers of keys should be letter,
# - dict's values should be a number (0-100),
# - example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
# 2. get previously generated list of dicts and create one common dict:
# - if dicts have same key, we will take max value, and rename key with dict number with max value
# - if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

import random
import string


def generate_random_dicts() -> list[dict]:
    """
    Generates a list of random dictionaries (from 2 to 10):
    - each dictionary has random letter keys (a–z)
    - each key maps to a random integer value (0–100)

    Returns:
        list[dict]: A list of randomly generated dictionaries
    """
    result_list = []

    # Randomly choose the number of dictionaries to generate (between 2 and 10 - according to task)
    dicts_number = random.randint(2, 10)

    # Iterate to generate chosen number of dictionaries
    for _ in range(dicts_number):
        # Randomly choose the number of elements in the dictionary (between 1 and 10)
        keys_number = random.randint(1, 10)

        # Randomly select unique lowercase (based on examples in the task) letters for keys
        random_keys = random.sample(string.ascii_lowercase, keys_number)

        # Assign a random value (0–100) to each key
        random_dict = {key: random.randint(0, 100) for key in random_keys}

        # Add the generated random dictionary to the result list
        result_list.append(random_dict)

    return result_list


# 2. get previously generated list of dicts and create one common dict:
# - if dicts have same key, we will take max value, and rename key with dict number with max value
# - if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

def merge_dicts(dict_list: list[dict]) -> dict:
    """
    Merges a list of dictionaries into one:
    - If a key appears in multiple dicts, keep the max value and tag key with dict number.
    - If a key appears only once, keep it as is.
    """
    key_sources = {}

    # Use enumerate to iterate through both index and dictionary
    for idx, random_dict in enumerate(dict_list):
        # Iterate through key_value pairs
        for key, value in random_dict.items():
            # For each entry of each key, map the key and a list of tuples containing both
            # the index of the random_dict where that key appears and the value of the key
            if key not in key_sources:
                # case for first key entry (add new dictionary item key: [(index, value)]
                # since index starts from 0, add +1 to get dictionary number
                key_sources[key] = [(idx + 1, value)]
            else:
                # case for second and further key entries
                key_sources[key].append((idx + 1, value))

    merged_dict = {}
    # Iterate through created dict items
    for key, sources in key_sources.items():
        if len(sources) == 1:
            # Key appeared only once
            merged_dict[key] = sources[0][1]
        else:
            # Key appeared multiple times
            # Find max_idx and max_val based on second element (key value)
            max_idx, max_val = max(sources, key=lambda x: x[1])
            # Take max value and add postfix with dict number to the key
            merged_dict[f"{key}_{max_idx}"] = max_val

    return merged_dict

# Check input - output
# random_dicts = generate_random_dicts()
# print(random_dicts)
# merged_dict = merge_dicts(random_dicts)
# print(merged_dict)
