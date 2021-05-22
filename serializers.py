import author as author
from rest_framework import serializers
from models import Book
from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source=author.username)

    class Meta:
        model = Book
        fields = ['date_of_publication', 'book_title', 'publisher', 'number_of_pages', 'author']


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'books']
