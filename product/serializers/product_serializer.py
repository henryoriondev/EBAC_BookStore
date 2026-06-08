from rest_framework import serializers

from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        many=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "category_id",
        ]

    def create(self, validated_data):
        categories = validated_data.pop("category")

        product = Product.objects.create(**validated_data)

        for category in categories:
            product.category.add(category)

        return product