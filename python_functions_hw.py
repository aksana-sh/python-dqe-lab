# Python Functions HW
# Refactor homeworks from module 2 and 3 using functional approach with decomposition

import random
import string
import re


# HW2 (Collections) decomposition
def generate_random_dict(max_items_number: int = 10) -> dict:
    """
    Generates a single random dictionary:
    - dictionary has random letter keys (a-z)
    - each key maps to a random value (0–100)

    Args:
        max_items_number (int, optional): The maximum number of items to generate.
            The actual number will be randomly chosen between 1 and max_items_number (inclusive). Default is 10.

    Returns:
        dict: Randomly generated dictionary
    """
    # Check for input parameter (26 unique lowercase letters)
    if not (1 <= max_items_number <= 26):
        raise ValueError("max_items_number must be between 1 and 26.")

    # Randomly choose the number of elements in the dictionary (between 1 and max_items_number(10 by default))
    keys_number = random.randint(1, max_items_number)

    # Randomly select unique lowercase letters for keys
    random_keys = random.sample(string.ascii_lowercase, keys_number)

    # Assign a random value (0–100) to each key
    random_dict = {key: random.randint(0, 100) for key in random_keys}

    return random_dict


def generate_random_dicts_list(
        min_dicts_number: int = 2,
        max_dicts_number: int = 10,
        max_dict_items_numer: int = 10) -> list[dict]:
    """
    Generates a list of randomly created dictionaries.

    Each dictionary contains:
    - Random lowercase letter keys (a–z)
    - Random integer values (0–100)

    Args:
        min_dicts_number (int, optional): The minimum number of dictionaries to generate. Default is 2.
        max_dicts_number (int, optional): The maximum number of dictionaries to generate. Default is 10.
            The actual number will be randomly chosen between min_dicts_number and max_dicts_number.
        max_dict_items_numer: The maximum number of items in random dictionaries. Default is 10.

    Returns:
        list[dict]: A list containing randomly generated dictionaries.
    """
    # Check for input parameters
    if min_dicts_number < 1 or max_dicts_number < min_dicts_number:
        raise ValueError("Invalid dictionary count range.")
    # Get number of dicts
    dicts_number = random.randint(min_dicts_number, max_dicts_number)
    # Generate random dicts
    return [generate_random_dict(max_dict_items_numer) for _ in range(dicts_number)]


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


# HW3 (Strings) decomposition
init_text = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


def extract_sentences(text: str) -> list[str]:
    """
    Extracts individual sentences from a given text using.
    A sentence is defined as a sequence of characters ending with a punctuation mark (.!?)

    Args:
        text (str): The input text to split into sentences.

    Returns:
        list[str]: A list of sentence strings extracted from the text.
    """
    return re.findall(r'[^.!?]*[.!?]', text)


def normalize_letter_case(text: str) -> str:
    """
    Normalizes the letter case of each sentence in the input text.

    For every sentence (ending with '.', '!', or '?'), the function:
    - Capitalizes the first alphabetical character.
    - Converts all other alphabetical characters in the sentence to lowercase.
    - Leaves punctuation and non-letter characters unchanged.

    Args:
        text (str): The input string.

    Returns:
        str: A new string with normalized letter casing for each sentence.
    """
    # Find sentences in a text by punctuation mark
    sentences = extract_sentences(text)

    normalized_sentences = []
    # Iterate over all the found sentences
    for sentence in sentences:
        # Converting sentence string (immutable) to list of chars (mutable)
        chars = list(sentence)
        first_letter_found = False
        # Use enumerate to iterate over both index and char
        for idx, char in enumerate(chars):
            # Check if char is alphabetical
            if char.isalpha():
                if not first_letter_found:
                    # Converting 1st letter to uppercase
                    chars[idx] = char.upper()
                    first_letter_found = True
                else:
                    # Converting not first letter to lowercase
                    chars[idx] = char.lower()
        # Join chars in a sentence
        normalized_sentences.append(''.join(chars))

    # Join sentences in a text
    normalized_text = ''.join(normalized_sentences)
    return normalized_text


def create_new_sentence(text: str) -> str:
    """
    Constructs a new sentence by extracting the last word from each sentence in the input text.

    Args:
        text (str): The input text containing one or more sentences.

    Returns:
        str: A newly constructed sentence made from the last words of each original sentence.
    """
    # Find sentences in a text by punctuation mark
    sentences = extract_sentences(text)
    # Extract last words from all sentences
    last_words = [re.findall(r'\b\w+\b', s)[-1] for s in sentences if re.findall(r'\b\w+\b', s)]
    # Combine last words into new sentence
    return ' '.join(last_words).capitalize() + '.'


def add_new_sentence(text: str, sentence_to_add: str, insert_after: str):
    """
    Inserts a new sentence into a specific location within the input text.

    The function performs the following steps:
    - Splits the input text into individual sentences using punctuation marks (., !, ?).
    - Searches for a sentence that contains a specific phrase (`insert_after`).
    - Appends the `sentence_to_add` to the end of the matching sentence.
    - Reconstructs and returns the modified text.

    Args:
        text (str): The original text containing one or more sentences.
        sentence_to_add (str): The sentence to be inserted.
        insert_after (str): A phrase used to locate the target sentence for insertion. The match is case-insensitive.

    Returns:
        str: The updated text with the new sentence inserted after the specified phrase.
    """
    # Find sentences in a text by punctuation mark
    sentences = extract_sentences(text)
    # Find the paragraph to insert new sentence
    for idx, sentence in enumerate(sentences):
        if insert_after.lower() in sentence.lower():
            # Insert the new sentence at the end of this paragraph
            sentences[idx] = sentence + ' ' + sentence_to_add

    # Reconstruct the full text
    return ''.join(sentences)


def fix_iz(text: str) -> str:
    """
    Corrects the common misspelling "iz" to "is" in a given text,
    but only when "iz" appears as a standalone word and is not enclosed in quotation marks.

    Args:
        text (str): The input text to process.

    Returns:
        str: The corrected text with "iz" replaced by "is".
    """
    return re.sub(r'(?<!["“‘])\b[Ii][Zz]\b(?!["”’])', 'is', text)


def count_whitespace(text: str) -> int:
    """
    Counts all whitespace characters in the given text (including Spaces, Tabs, Newlines, etc.)

    Args:
        text (str): The input text.

    Returns:
        int: The total number of whitespace characters found in the text.
    """
    # Count all whitespace characters
    return len(re.findall(r'\s', text))


# HW2 Collections:
# print(generate_random_dict())
# print(generate_random_dict(1))
# print(generate_random_dicts_list())
# test_dict = generate_random_dicts_list(2,2)
# print(test_dict)
# print(merge_dicts(test_dict))

# HW3 Strings:
# print(extract_sentences(init_text))
# normalized_case = normalize_letter_case(init_text)
# print(normalized_case)
# new_sentence = create_new_sentence(normalized_case)
# print(new_sentence)
# added_text = (add_new_sentence(normalized_case, new_sentence, "TEXT to variable"))
# print(added_text)
# print(fix_iz(added_text))
# print(count_whitespace(init_text))
