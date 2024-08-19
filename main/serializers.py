from rest_framework import serializers
import json
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
        fields = ('id', 'book_details', 'word', 'testing_word_list', 'page_list', 'status')

        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['page_list'] = instance.get_page_list()
        representation['testing_word_list'] = instance.get_testing_word_list()
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['page_list'] = json.dumps(internal_value['page_list'])
        internal_value['testing_word_list'] = json.dumps(internal_value['testing_word_list'])
        return internal_value


class CheckWordSerializer(serializers.Serializer):
    letter = serializers.CharField(max_length=50)
    page_number = serializers.IntegerField()
    book_id = serializers.IntegerField()
    