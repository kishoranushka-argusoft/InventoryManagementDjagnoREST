from .models import Products, Category, Sellers, Transactions
from rest_framework import serializers
from datetime import datetime


# class ProductSerializer(serializers.ModelSerializer):

#     category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), write_only= True)

#     seller = serializers.PrimaryKeyRelatedField(queryset = Sellers.objects.all(), write_only = True, many=True)

#     categoryname = serializers.CharField(source= "category.name")
#     sellernames = serializers.StringRelatedField(many=True)
#     class Meta:
#         model= Products
#         fields = ["id","category","categoryname","seller","sellernames","name", "price","weight","expiry_date","quantity_in_stock","image","created_at","updated_at"]

    # def create(self, validated_data):
    #     category = validated_data["category"]
    #     seller = validated_data["seller"]

    #     cat_id = category.id
    #     seller_id = seller.id

    #     validated_data["category"] = cat_id
    #     validated_data["seller"] = seller_id

    #     category.save()
    #     seller.save()

    #     return super().create(validated_data)

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model= Category
        fields = "__all__"

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sellers
        fields = "__all__"

class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)   
    seller = SellerSerializer(many=True, read_only=True)
    class Meta:
        model= Products
        fields = "__all__"

class ProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset= Category.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Sellers.objects.all(), many=True)
    image = serializers.ImageField(required=False)
    class Meta:
        model = Products
        fields = "__all__"


    def to_internal_value(self, data):
    # Handle seller field when it comes from FormData
        if hasattr(data, 'getlist'):
            seller_list = data.getlist('seller')
            data = data.copy()
            data.setlist('seller', seller_list)
        else:
            seller = data.get("seller")
            if seller and not isinstance(seller, list):
                data["seller"] = [seller]

        expiry_date = data.get("expiry_date")
        if expiry_date and len(expiry_date) == 10:
            try:
                data["expiry_date"]= datetime.strptime(expiry_date, "%Y-%m-%d").isoformat()+ "Z"
            except Exception:
                pass
        return super().to_internal_value(data)
    


class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all())
    product_name = serializers.CharField(source="product.name", read_only=True)


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