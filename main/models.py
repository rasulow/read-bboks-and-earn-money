from django.db import models
from django.conf import settings
from account.models import User
from django.utils.timesince import timesince
from typing import List
from PyPDF2 import PdfReader
import io
import json
from .managers import PurchaseManager



class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(default='Empty')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Genre(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Author')
    description = models.TextField(default='...')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    book = models.FileField(upload_to='books', max_length=500)
    pages = models.IntegerField(default=0)
    image = models.ImageField(upload_to='books_images', max_length=500)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Genre')
    published_at = models.CharField(max_length=4, default='....')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    rating_count = models.IntegerField(default=0)
    favourites_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)

    def get_book(self):
        if self.book:
            return self.book.url
        else:
            return ''

    def get_book_ext(self):
        ext = self.book.name.split('.')[-1]
        return f".{ext}"

    def get_book_size(self):
        size_in_mb = self.book.size / (1024 * 1024)
        return "{:.2f} Mb".format(size_in_mb)

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
    def get_page_number(self):
        pdf_reader = PdfReader(io.BytesIO(self.book.read()))
        return len(pdf_reader.pages)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')
    word = models.CharField(max_length=50, blank=True, null=True)
    testing_word = models.CharField(max_length=50, blank=True, null=True)
    testing_word_list = models.CharField(max_length=50, blank=True, null=True)
    page_list = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.book)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)
    
    def set_page_list(self, page_list: list[int] = []):
        self.page_list = json.dumps(page_list)

    def get_page_list(self) -> list[int]:
        return json.loads(self.page_list) if self.page_list else []

    def set_testing_word_list(self, word_list: list[str] = []):
        self.testing_word_list = json.dumps(word_list)

    def get_testing_word_list(self) -> list[str]:
        return json.loads(self.testing_word_list) if self.testing_word_list else []
    
    def delete_page_at_index(self, index: int, letter: str) -> bool:
        try:
            page_list = self.get_page_list()
            testing_word_list = self.get_testing_word_list()

            if self.testing_word[index].upper() != letter.upper():
                return False

            testing_word_list.insert(index, letter.upper())
            page_list[index] = 0
            self.set_page_list(page_list)
            self.set_testing_word_list(testing_word_list)
            self.save()
            return True

        except (IndexError, ValueError) as e:
            raise ValueError(f"Error at index {index}: {str(e)}")
    
    def save(self, *args, **kwargs):
        if not self.word:
            from utils.words import get_random_word, generate_page_nums_for_word
            
            random_word = get_random_word()
            self.word = random_word
            self.testing_word = random_word
            
            book_page_num = self.book.get_page_number()
            word_len = len(random_word)
            page_nums = generate_page_nums_for_word(book_page_num, word_len)
            
            self.set_page_list(page_nums)
            print(1111111111111)
            self.set_testing_word_list(['' for _ in range(word_len)])
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def updated_at_formatted(self):
        return timesince(self.updated_at)

    class Meta:
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'

