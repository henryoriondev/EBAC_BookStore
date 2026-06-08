import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers import CategorySerializer, ProductSerializer


@pytest.mark.django_db
def test_category_serializer():
    category = CategoryFactory(
        title="Programação",
        slug="programacao",
        description="Livros de programação",
        active=True,
    )

    serializer = CategorySerializer(category)

    assert serializer.data["title"] == "Programação"
    assert serializer.data["slug"] == "programacao"
    assert serializer.data["description"] == "Livros de programação"
    assert serializer.data["active"] is True


@pytest.mark.django_db
def test_product_serializer():
    category = CategoryFactory(
        title="Backend",
        slug="backend",
        description="Categoria backend",
        active=True,
    )

    product = ProductFactory(
        title="Django API",
        description="Livro sobre Django REST",
        price=100,
        active=True,
        category=[category],
    )

    serializer = ProductSerializer(product)

    assert serializer.data["title"] == "Django API"
    assert serializer.data["description"] == "Livro sobre Django REST"
    assert serializer.data["price"] == 100
    assert serializer.data["active"] is True
    assert serializer.data["category"][0]["title"] == "Backend"
    assert serializer.data["category"][0]["slug"] == "backend"