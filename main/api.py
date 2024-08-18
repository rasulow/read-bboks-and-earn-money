from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .serializers import (
    BookSerializer,
    AuthorSerializer,
    GenreSerializer,
    FavouriteSerializer,
    PurchaseSerializer,
    CheckWordSerializer,
    PurchaseListSerializer
)

from .models import (
    Book,
    Author,
    Genre,
    Favourite,
    Purchase,
)

from account.models import User
from utils.pagination import MyCustomPagination



# * Book related
class BookListView(APIView):
    permission_classes = [AllowAny]
    

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'author', openapi.IN_QUERY, description="Filter by author", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search...", type=openapi.TYPE_STRING
            ),
        ],
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request):
        books = Book.objects.all()

        author = request.GET.get('author')
        genre = request.GET.get('genre')
        search = request.GET.get('search')
        
        if author:
            books = books.filter(author__id=int(author))
        if genre:
            books = books.filter(genre__id=int(genre))
        if search:
            books = books.filter(title__icontains=search) | books.filter(description__icontains=search)

        paginator = MyCustomPagination()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)

        return paginator.get_paginated_response(serializer.data)
    

class BookDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        response_data = serializer.data

        if request.user.is_authenticated:
            purchased = Purchase.objects.filter(user=request.user, book=book).exists()
            response_data['purchased'] = purchased
        else:
            response_data['purchased'] = False

        return Response(response_data)
        


class LikeBookView(APIView):

    def post(self, request, pk):
        user = request.user
        book = get_object_or_404(Book, pk=pk)

        try:
            favourite = Favourite.objects.get(user=user, book=book)
            favourite.delete()
            return Response({'message': 'Book unliked'}, status=status.HTTP_200_OK)
        except Favourite.DoesNotExist:
            Favourite.objects.create(user=user, book=book)
            return Response({'message': 'Book liked'}, status=status.HTTP_200_OK)


class UserFavouriteBooksView(APIView):
    
    def get(self, request):
        user = request.user
        favourites = Favourite.objects.filter(user=user)
        paginator = MyCustomPagination()
        paginated_favourites = paginator.paginate_queryset(favourites, request)
        serializer = FavouriteSerializer(paginated_favourites, many=True)

        return paginator.get_paginated_response(serializer.data)
    

    @swagger_auto_schema(
        request_body=PurchaseSerializer,
        responses={
            201: openapi.Response('Favourite added successful', PurchaseSerializer),
            400: 'Bad Request'}
    )
    def post(self, request):
        user = request.user
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            book = Book.objects.get(id=book_id)
            if Favourite.objects.filter(user=user, book=book).exists():
                Favourite.objects.filter(user=user, book=book).delete()
                return Response({'status': 'deleted', 'message': 'This book has already been favourited'}, status=status.HTTP_200_OK)
            favourite = Favourite.objects.create(user=user, book=book)
            response = {
                'status': 'addedd', 
                'message': 'Favourite added successfully',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



# * Author related
class AuthorListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        authors = Author.objects.all()
        paginator = MyCustomPagination()
        paginated_authors = paginator.paginate_queryset(authors, request)
        serializer = AuthorSerializer(paginated_authors, many=True)

        return paginator.get_paginated_response(serializer.data)


class AuthorDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author)

        return Response(serializer.data)



# * Genre related
class GenreListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        return Response(serializer.data)


    


# * Purchase related
class PurchaseBookView(APIView):
    @swagger_auto_schema(
        request_body=PurchaseSerializer,
        responses={
            201: openapi.Response('Purchase successful', PurchaseSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        user = request.user
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            book = get_object_or_404(Book, id=book_id)
            if Purchase.objects.filter(user=user, book=book).exists():
                return Response({'message': 'This book has already been purchased'}, status=status.HTTP_200_OK)
            purchase = Purchase.objects.create(user=user, book=book)
            response = {
                'word': purchase.word,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        user = request.user
        purchases = Purchase.objects.filter(user=user)
        paginator = MyCustomPagination()
        paginated_purchases = paginator.paginate_queryset(purchases, request)
        serializer = PurchaseListSerializer(paginated_purchases, many=True)
        return paginator.get_paginated_response(serializer.data)
        



class CheckWord(APIView):

    @swagger_auto_schema(
        request_body=CheckWordSerializer,
        responses={
            200: openapi.Response('Word checked successfully', CheckWordSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        user = request.user
        serializer = CheckWordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_id = serializer.validated_data['book_id']
        page_number = serializer.validated_data['page_number']
        letter = serializer.validated_data['letter'].upper()  # Ensure letter is uppercase

        book = get_object_or_404(Book, id=book_id)
        purchased = get_object_or_404(Purchase, book=book, user=user)

        if not purchased.status:
            return Response({'message': f'Congratulations! You guessed the word. Your balance is {user.balance}'}, status=status.HTTP_200_OK)

        # Find the index of the letter to be replaced
        page_list = purchased.get_page_list()
        replaced_index = page_list.index(page_number)
        if replaced_index == -1:
            return Response({'message': 'Letter not found in testing word.'}, status=status.HTTP_400_BAD_REQUEST)

        # Replace the first occurrence of the letter
        replace_page_number = purchased.delete_page_at_index(replaced_index, letter)
        if not replace_page_number:
            return Response({'message': 'Letter and page number don\'t match!'}, status=status.HTTP_400_BAD_REQUEST)
        purchased.testing_word = purchased.testing_word[:replaced_index] + ' ' + purchased.testing_word[replaced_index + 1:]

        if not purchased.testing_word:
            purchased.status = False
            user.balance += 5
            user.save()
            purchased.save()
            return Response({
                'message': f'Congratulations! You guessed the word. Your balance is {user.balance}',
            }, status=status.HTTP_200_OK)
        
        purchased.save()
        return Response({'testing_word': purchased.testing_word, 'replaced_index': replaced_index}, status=status.HTTP_200_OK)
