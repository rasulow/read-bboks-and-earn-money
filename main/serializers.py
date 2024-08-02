from rest_framework import serializers
from .models import (
    Book,
    Author,
    Genre,
    Favourite,
    Purchase
)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'biography', 'created_at_formatted',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'created_at_formatted',)


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'description',
            'price',
            'get_book',
            'get_book_ext',
            'get_book_size',
            'get_image',
            'get_page_number',
            'genre',
            'published_at',
            'created_at',
            'rating_count',
            'favourites_count',
        )


class FavouriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = ('id', 'user', 'book', 'created_at_formatted',)



class PurchaseSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()


class PurchaseListSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)

    class Meta:
        model = Purchase
        fields = ('book_details',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        book_representation = representation.pop('book_details')
        for key, value in book_representation.items():
            representation[key] = value
        return representation


class CheckWordSerializer(serializers.Serializer):
    letter = serializers.CharField(max_length=50)
    book_id = serializers.IntegerField()
    