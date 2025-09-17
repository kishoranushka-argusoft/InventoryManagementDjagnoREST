from .models import Products, Category, Sellers, Transactions
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source= "category.name", read_only=True)
    seller = serializers.StringRelatedField(many=True)
    class Meta:
        model= Products
        fields = "__all__"
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = "__all__"

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sellers
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source= "product.name", read_only=True)

    class Meta:
        model= Transactions
        fields = "__all__"
        read_ony_fields =("price_per_unit","total_price","transaction_date")

    def create(self, validated_data):
        # print("@@@@@@@@@@@@@@@@@", validated_data)
        product = validated_data["product"]
        quantity = validated_data["quantity"]
        transactions_type = validated_data["transactions_type"]

        unit_price=product.price
        total_price = unit_price*quantity

        validated_data["price_per_unit"]= unit_price
        validated_data["total_price"] = total_price

        if transactions_type == 'S':
            if product.quantity_in_stock<quantity:
                raise serializers.ValidationError({"quantity": "Not enough stock available"})
            product.quantity_in_stock -= quantity

        elif transactions_type in ['A', 'R']:
            product.quantity_in_stock += quantity
        product.save()

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        product = validated_data.get("product", instance.product)
        quantity = validated_data.get("quantity", instance.quantity)
        transactions_type = validated_data.get("transactions_type", instance.transactions_type)

        unit_price = product.price
        total_price = unit_price*quantity

        validated_data["price_per_unit"] = unit_price
        validated_data["total_price"]= total_price

        return super().update(instance,validated_data)