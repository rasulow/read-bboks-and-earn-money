from django.urls import path, include
from . import api

urlpatterns = [
    path('v1/', include([
        # Book-related endpoints
        path('books/', api.BookListView.as_view(), name='book_list'),
        path('books/<int:pk>/', api.BookDetail.as_view(), name='book_detail'),
        path('books/<int:pk>/like/', api.LikeBookView.as_view(), name='like_book'),
        path('books/favourites/', api.UserFavouriteBooksView.as_view(), name='user_favourite_books'),
        path('books/favourites/<int:id>/', api.UserFavouriteDelete.as_view(), name='user_favourite_delete'),

        # Author-related endpoints
        path('authors/', api.AuthorListView.as_view(), name='author_list'),
        path('authors/<int:pk>/', api.AuthorDetailView.as_view(), name='author_detail'),

        # Genre-related endpoints
        path('genres/', api.GenreListView.as_view(), name='genre_list'),

        # Purchase-related endpoint
        path('purchase-book/', api.PurchaseBookView.as_view(), name='purchase'),
        path('book/word-check/', api.CheckWord.as_view(), name='word-check')
    ])),
]