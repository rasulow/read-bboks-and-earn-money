import random
from typing import List
from pathlib import Path



_words_cache = None

def get_random_word() -> str:
    global _words_cache
    if _words_cache is None:
        current_dir = Path(__file__).parent
        file_path = current_dir / 'words.txt'
        try:
            with file_path.open('r') as f:
                _words_cache = f.read().splitlines()
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
    
    return random.choice(_words_cache).upper()
    


def generate_page_nums_for_word(book_page_num: int, word_len: int) -> List[int]:
    start_index = random.randint(20, 30)
    end_index = random.randint(book_page_num - 20, book_page_num - 10)

    page_nums = set()

    while len(page_nums) < word_len - 2:
        num = random.randint(start_index + 10, end_index - 10)
        if num not in page_nums:
            page_nums.add(num)

    page_nums = list(page_nums)
    page_nums.append(start_index)
    page_nums.append(end_index)

    return sorted(page_nums)