#!/usr/bin/env python3

import os
import string
from typing import Dict

directory_path = os.getcwd()+'/wiki/'

# List to store all dictionaries (each corresponding to a file)
file_dicts = []

# Collect all text files in the directory
text_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

# For each file, create a dictionary of word frequencies
for file in text_files:
    with open(os.path.join(directory_path, file), 'r') as f:
        text = f.read().lower()
        # remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        word_freq: Dict[str,int] = {}
        for word in words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
        file_dicts.append(word_freq)

# Determine the threshold for word appearance in files
threshold = len(text_files) * 0.5

# Count the number of files each word appears in
word_file_count: Dict[str,int] = {}
for word_dict in file_dicts:
    for word in word_dict.keys():
        if word not in word_file_count:
            word_file_count[word] = 1
        else:    
            word_file_count[word] += 1

# Filter words that appear in 50% or more of the files
for word_dict in file_dicts:
    for word in list(word_dict.keys()):  # Create a list from keys to avoid 'dictionary changed size during iteration' error
        if word_file_count[word] >= threshold:
            del word_dict[word]

# Now, file_dicts contains the frequency dictionaries for each file, 
# with words appearing in 50% or more of the files removed
