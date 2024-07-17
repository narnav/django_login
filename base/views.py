from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



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





@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def product(request, id=None):
    if request.method == 'GET':
        if id is not None:
            product = get_object_or_404(Product, pk=id) #single
            return Response({
                'id': product.id,
                'desc': product.desc,
                'price': str(product.price),
                'createdTime': product.createdTime.isoformat(),
            })
        else:
            products = Product.objects.all() # all
            data = []
            for product in products:
                data.append({
                    'id': product.id,
                    'desc': product.desc,
                    'price': str(product.price),
                    'createdTime': product.createdTime.isoformat(),
                })
            return Response(data)
    
    elif request.method == 'POST':
        desc = request.data.get('desc', '')
        price = request.data.get('price', '0.00')
        try:
            price = Decimal(price)
        except Decimal.InvalidOperation:
            return Response({'error': 'Invalid price format'}, status=400)
        
        new_product = Product(desc=desc, price=price)
        new_product.save()
        return Response({'message': 'Product created successfully', 'id': new_product.id})
    
    elif request.method in ['PUT', 'PATCH']:
        product = get_object_or_404(Product, pk=id)
        desc = request.data.get('desc', product.desc)
        price = request.data.get('price', product.price)
        try:
            price = Decimal(price)
        except Decimal.InvalidOperation:
            return Response({'error': 'Invalid price format'}, status=400)
        
        product.desc = desc
        product.price = price
        product.save()
        return Response({'message': 'Product updated successfully'})
    
    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response({'message': 'Product deleted successfully'})
    
    return Response({'error': 'Method not allowed'}, status=405)


