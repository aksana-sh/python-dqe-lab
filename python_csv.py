# Python CSV Parsing.
# Calculate number of words and letters from previous Homeworks 5/6 output test file.
# Create two csv:
# 1.word-count (all words are preprocessed in lowercase)
# 2.letter, count_all, count_uppercase, percentage (add header, space characters are not included)
# CSVs should be recreated each time new record added.

import csv
import re
from collections import Counter
import os


def count_words(file_path=None):
    """
    Reads a text file and writes word counts to csv file.
    Uses current directory and 'news_feed.txt' as default if no path is provided.
    """
    # Use default file in current directory if no path is provided
    if file_path is None:
        file_path = os.path.join(os.getcwd(), "news_feed.txt")

    # Read input file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract words and convert to lowercase (no dates, numbers)
    words = re.findall(r"\b[a-zA-Z']+\b", content.lower())

    # Count words
    # word_counts = {}
    # for word in words:
    #     word_counts[word] = word_counts.get(word, 0) + 1

    # Count words
    word_counts = Counter(words)

    # Write word counts to word-count.csv output file (no header, hyphen as column separator)
    with open("word-count.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='-')
        for word, count in word_counts.items():
            writer.writerow([word, count])


def count_letters(file_path=None):
    """
    Reads a text file and writes letter statistics (total count, uppercase count, and percentage) to csv file
    Uses current directory and 'news_feed.txt' as default if no path is provided.
    """
    # Use default file in current directory if no path is provided
    if file_path is None:
        file_path = os.path.join(os.getcwd(), "news_feed.txt")

    # Read input file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Get only alphabetic characters (no spaces, digits, punctuation)
    letters = re.findall(r'[A-Za-z]', content)

    # Count lowercase and uppercase letters
    letter_counts = Counter(letters)  # case-sensitive

    # Total number of all letters
    total_letters = sum(letter_counts.values())

    # Preparation to writing to file
    with open("letter-count.csv", "w", newline='', encoding="utf-8") as f:
        header = ["letter", "count_all", "count_uppercase", "percentage"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

        # Loop through unique lowercase letters
        for letter in sorted(set(l.lower() for l in letters)):
            # for each letter count required metrics: all, uppercase, percentage
            count_lower = letter_counts.get(letter.lower(), 0)
            count_upper = letter_counts.get(letter.upper(), 0)
            count_all = count_lower + count_upper
            percentage = round((count_all / total_letters) * 100, 2)

            # Write row as dictionary
            writer.writerow({
                "letter": letter,
                "count_all": count_all,
                "count_uppercase": count_upper,
                "percentage": percentage
            })

# count_words()
# count_letters()