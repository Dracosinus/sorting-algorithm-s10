import os
import string
from typing import Dict

directory_path = os.getcwd()+'/wiki/'

# Dict to store all dictionaries (each corresponding to a file)
file_dicts: Dict[str, Dict[str, int]] = {}

# Collect all text files in the directory
text_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

# For each file, create a dictionary of word frequencies
for file in text_files:
    with open(os.path.join(directory_path, file), 'r') as f:
        text = f.read().lower()
        # remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        word_freq: Dict[str, int] = {}
        for word in words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
        file_dicts[file] = word_freq

# Determine the threshold for word appearance in files
higher_threshold = len(text_files) * 0.5
lower_treshhold = len(text_files) * 0.1

# Count the number of files each word appears in
word_file_count: Dict[str, int] = {}
for word_dict in file_dicts.values():
    for word in word_dict.keys():
        if word not in word_file_count:
            word_file_count[word] = 1
        else:
            word_file_count[word] += 1

# Filter words that appear in 50% or more of the files
for word_dict in file_dicts.values():
    for word in list(word_dict.keys()):
        if word_file_count[word] >= higher_threshold:
            del word_dict[word]
        if word_file_count[word] <= lower_treshhold:
            del word_dict[word]

FILE_DICTS = file_dicts
