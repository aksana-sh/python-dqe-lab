# Python Strings HW

import re

init_text = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


# Step 1: Normalize text from letter case point of view
# Since the task says to change only the letter case, we need to preserve the structure of the original text
def normalize_letter_case(text):
    # Find sentences in a text by punctuation mark
    sentences = re.findall(r'[^.!?]*[.!?]', text)

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


# Step 2: Add new sentence to the end of the paragraph with this task
def add_new_sentence(text):
    # Find sentences in a text by punctuation mark
    sentences = re.findall(r'[^.!?]*[.!?]', text)
    # Extract last words from all sentences
    last_words = [re.findall(r'\b\w+\b', s)[-1] for s in sentences if re.findall(r'\b\w+\b', s)]
    # Combine last words into new sentence
    new_sentence = ' '.join(last_words).capitalize() + '.'

    # Find the paragraph to insert new sentence
    for idx, sentence in enumerate(sentences):
        if "create one more sentence with last words" in sentence.lower():
            # Insert the new sentence at the end of this paragraph
            sentences[idx] = sentence + ' ' + new_sentence

    # Reconstruct the full text
    return ''.join(sentences)


# Step 3: Fix incorrect "iz" → "is" only when it's a mistake
def fix_iz(text):
    # Replace standalone iz only when it's NOT inside quotes
    return re.sub(r'(?<!["“‘])\b[Ii][Zz]\b(?!["”’])', 'is', text)


# Step 4: Count all whitespace characters (including regular space, new line, nbsp, etc.)
def count_whitespace(text):
    # Count all whitespace characters
    return len(re.findall(r'\s', text))


# Check input - output
# normalized_text = normalize_letter_case(init_text)
# print(normalized_text)
#
# added_text = (add_new_sentence(normalized_text))
# print(added_text)
#
# fixed_text = fix_iz(added_text)
# print(fixed_text)
#
# whitespaces_cnt = count_whitespace(init_text)
# print(whitespaces_cnt)




