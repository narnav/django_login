
from django.shortcuts import get_object_or_404
from .models import Product,Book
from decimal import Decimal
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers

# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                last_name=request.data['last_name']
            )
    user.is_active = False
    user.is_staff = False
    user.is_superuser = True
    user.save()
    return Response("new user born")

@api_view(['GET'])
def index(req):
    return Response({'test':'msg'})

@api_view(['GET'])
def test(req):
    return Response({'test':'success'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member(req):
    return Response({'members':'only'})

@api_view(['GET'])
def allpub(req):
    return Response({'test':'public'})

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product(request, id=None):
    if request.method == 'GET':
        if id is not None:
            product = get_object_or_404(Product, pk=id) #single
            return Response (ProductSerializer(product,many=False).data)
        else:
            return Response (ProductSerializer(Product.objects.all(),many=True).data)
    
    elif request.method == 'POST':
        prod_serializer = ProductSerializer(data=request.data)
        if prod_serializer.is_valid():
            prod_serializer.save()
            return Response ({'message': 'Product created successfully'})
        else:
            return Response (prod_serializer.errors)
    
    elif request.method in ['PUT', 'PATCH']:
        try:
            product=Product.objects.get(id=id)
        except product.DoesNotExist:
            return Response ("not found")
       
        ser = ProductSerializer(data=request.data)
        old_task = Product.objects.get(id=id)
        ser.update(old_task, request.data)
        return Response('upd')

    elif request.method == 'DELETE':
        try:
            product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")    
        product.delete()
        return Response ({'message': 'Product caput successfully'})



@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def book_view(request, id=None):
    if request.method == 'GET':
        if id is not None:
            book = get_object_or_404(Book, pk=id) #single
            return Response (BookSerializer(book,many=False).data)
        else:
            return Response (BookSerializer(Book.objects.all(),many=True).data)
    
    elif request.method == 'POST':
        prod_serializer = BookSerializer(data=request.data)
        if prod_serializer.is_valid():
            prod_serializer.save()
            return Response ({'message': 'book created successfully'})
        else:
            return Response (prod_serializer.errors)
    
    elif request.method in ['PUT', 'PATCH']:
        try:
            book=Book.objects.get(id=id)
        except book.DoesNotExist:
            return Response ("not found")
       
        ser = BookSerializer(data=request.data)
        old_task = Book.objects.get(id=id)
        ser.update(old_task, request.data)
        return Response('upd')

    elif request.method == 'DELETE':
        try:
            book=Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response ("not found")    
        book.delete()
        return Response ({'message': 'book caput successfully'})


