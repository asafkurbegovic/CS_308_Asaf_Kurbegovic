from models import Book
from serializers import BookSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly


class BookList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        book = self.get_object(id)
        serializer = BookSerializer(Book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class AuthorsList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorsDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
