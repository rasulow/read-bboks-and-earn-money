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
    PurchaseSerializer
)

from .models import (
    Book,
    Author,
    Genre,
    Favourite,
    Purchase,
)

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
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return JsonResponse(serializer.data)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book does not exist'}, status=404)
        


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
            book = get_object_or_404(Book, id=book_id)
            favourite = Favourite.objects.create(user=user, book=book)
            response = {
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
            purchase = Purchase.objects.create(user=user, book=book)
            response = {
                'word': purchase.word,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)