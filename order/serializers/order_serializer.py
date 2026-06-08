from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
        many=True,
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "product",
            "product_id",
            "total",
        ]

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())

    def create(self, validated_data):
        products = validated_data.pop("product")

        order = Order.objects.create(**validated_data)

        order.product.set(products)

        return order