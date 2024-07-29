import os
import random


def get_random_word():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'words.txt')
    with open(file_path, 'r') as f:
        words = f.read().splitlines()
        return random.choice(words).upper()