from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Genre, Book, Author
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PyPDF2 import PdfWriter

class GenreListViewTest(APITestCase):
    def setUp(self):
        # Create some Genre instances
        self.genre1 = Genre.objects.create(name="Rock")
        self.genre2 = Genre.objects.create(name="Jazz")

    def test_genre_list(self):
        url = reverse('genre_list')
        response = self.client.get(url)
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Parse the response data
        genres = response.json()
        
        # Ensure the correct number of genres is returned
        self.assertEqual(len(genres), 2)
        
        # Check that the genre data matches
        self.assertEqual(genres[0]['name'], self.genre1.name)
        self.assertEqual(genres[1]['name'], self.genre2.name)
        
        # Check that the 'created_at_formatted' field is present
        self.assertIn('created_at_formatted', genres[0])
        self.assertIn('created_at_formatted', genres[1])
        
        
    
class BookListViewTest(APITestCase):
    def setUp(self):
        # Create a sample PDF file for testing
        pdf_writer = PdfWriter()
        pdf_writer.add_blank_page(width=72, height=72)
        pdf_buffer = io.BytesIO()
        pdf_writer.write(pdf_buffer)
        pdf_buffer.seek(0)
        
        self.sample_pdf = SimpleUploadedFile("sample.pdf", pdf_buffer.read(), content_type="application/pdf")
        self.sample_image = SimpleUploadedFile("sample.jpg", b"image_content", content_type="image/jpeg")

        # Create instances for testing
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        
        self.genre1 = Genre.objects.create(name="Fiction")
        self.genre2 = Genre.objects.create(name="Non-Fiction")
        
        self.book1 = Book.objects.create(
            title="Book One", 
            author=self.author1, 
            description="A great book", 
            price=10.99,
            book=self.sample_pdf,
            image=self.sample_image,
            genre=self.genre1,
            published_at="2023",
        )
        self.book2 = Book.objects.create(
            title="Book Two", 
            author=self.author2, 
            description="Another great book", 
            price=15.99,
            book=self.sample_pdf,
            image=self.sample_image,
            genre=self.genre2,
            published_at="2024",
        )
    
    def test_book_list(self):
        url = reverse('book_list')
        response = self.client.get(url)
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the correct number of books is returned
        books = response.json()['results']
        self.assertEqual(len(books), 2)

        # Check if custom methods are present in the response
        self.assertIn('get_book', books[0])
        self.assertIn('get_book_ext', books[0])
        self.assertIn('get_book_size', books[0])
        self.assertIn('get_image', books[0])
        self.assertIn('get_page_number', books[0])
    
    def test_book_filter_by_author(self):
        url = reverse('book_list')
        response = self.client.get(url, {'author': self.author1.id})
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure only one book is returned and it's the correct one
        books = response.json()['results']
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['author']['name'], self.author1.name)

    def test_book_filter_by_genre(self):
        url = reverse('book_list')
        response = self.client.get(url, {'genre': self.genre1.id})
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure only one book is returned and it's the correct one
        books = response.json()['results']
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['genre']['name'], self.genre1.name)
        
    def test_book_search(self):
        url = reverse('book_list')
        response = self.client.get(url, {'search': 'great'})
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure two books are returned as both contain 'great' in description
        books = response.json()['results']
        self.assertEqual(len(books), 2)
        self.assertTrue(any(book['title'] == self.book1.title for book in books))
        self.assertTrue(any(book['title'] == self.book2.title for book in books))
        url = reverse('book_list')
        response = self.client.get(url, {'search': 'great'})
        
        # Ensure the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure two books are returned as both contain 'great' in description
        books = response.json()['results']
        self.assertEqual(len(books), 2)
        self.assertTrue(any(book['title'] == self.book1.title for book in books))
        self.assertTrue(any(book['title'] == self.book2.title for book in books))