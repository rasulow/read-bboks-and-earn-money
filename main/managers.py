from django.db import models
from utils.words import get_random_word, generate_page_nums_for_word



class PurchaseManager(models.Manager):
    def create(self, user, book, word=None, testing_word=None, testing_word_list=None, page_list=None, status=True, **extra_fields):
        # Add any custom logic here
        random_word = get_random_word()
        self.word = random_word
        self.testing_word = random_word
        
        book_page_num = self.book.get_page_number()
        word_len = len(random_word)
        page_nums = generate_page_nums_for_word(book_page_num, word_len)
        
        self.set_page_list(page_nums)
        self.set_testing_word_list(['' for _ in range(word_len)])

        purchase = self.model(
            user=user,
            book=book,
            word=word,
            testing_word=testing_word,
            testing_word_list=testing_word_list,
            page_list=page_list,
            status=status,
            **extra_fields
        )
        purchase.save(using=self._db)
        return purchase