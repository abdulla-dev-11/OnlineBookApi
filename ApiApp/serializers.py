from rest_framework import serializers
from ApiApp.models import Author, Book, Order, OrderItem


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date', 'biography', 'books_count']

    def get_books_count(self, obj):
        return obj.books.count()


class BookSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'stock', 'is_in_stock']

    def get_is_in_stock(self, obj):
        return obj.stock > 0


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.book.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'books', 'created_at', 'total_price', 'subtotal']

    def get_subtotal(self, obj):
        return sum(item.book.price * item.quantity for item in obj.order_items.all())

    def get_user(self, obj):
        return obj.user

