from .models import Products, Category, Sellers, Transactions
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    class Meta:
        model= Products
        fields = "__all__"

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        return Products.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = "__all__"

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sellers
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Transactions
        fields = "__all__"