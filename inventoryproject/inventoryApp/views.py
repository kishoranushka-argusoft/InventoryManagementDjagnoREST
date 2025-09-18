from django.shortcuts import render
from rest_framework.response import Response
from .models import Products, Category, Sellers, Transactions
from rest_framework.decorators import api_view
from .serializers import ProductReadSerializer, ProductWriteSerializer, CategorySerializer, SellerSerializer, TransactionSerializer
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductReadSerializer(products, many=True)
        print("🐍 File: inventoryApp/views.py | Line: 16 | products_view ~ serializer",serializer)
        print("--------------",serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductWriteSerializer(data = request.data)
        print("🐍 File: inventoryApp/views.py | Line: 22 | products_view ~ serializer",serializer)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print("&&&&&&&&&&&&&&&&&&&&&&", validated_data)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
def product_detail_view(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductReadSerializer(product)
        print("******************", serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProductWriteSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def categories_view(request):
    if request.method == 'GET':
        categoies = Category.objects.all()
        serializer = CategorySerializer(categoies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
def category_detail_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def seller_view(request):
    if request.method== 'GET':
        sellers = Sellers.objects.all()
        serializer = SellerSerializer(sellers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    elif request.method == 'POST':
        serializer = SellerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT', 'DELETE'])
def seller_detail_view(request, pk):
    try:
        seller = Sellers.objects.get(pk=pk)
    except Sellers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(seller)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(seller, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])
def transactions_view(request):
    if request.method =='GET':
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions, many= True)
        print("🐍 File: inventoryApp/views.py | Line: 138 | transactions_view ~ serializer",serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = TransactionSerializer(data= request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # print("^^^^^^^^^^^^^^^^^^^^^^^",validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            print("****************", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT', 'DELETE'])
def transaction_detail_view(request, pk):
    try:
        transaction = Transactions.objects.get(pk=pk)
    except Transactions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = TransactionSerializer(transaction)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = TransactionSerializer(transaction, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == "DELETE":
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)