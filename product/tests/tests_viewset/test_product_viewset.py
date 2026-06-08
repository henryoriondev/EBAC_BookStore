import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from product.factories import ProductFactory, CategoryFactory


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def api_client(user):
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {token.key}"
    )

    return client


@pytest.mark.django_db
def test_list_products_authenticated(api_client):
    ProductFactory.create_batch(3)

    response = api_client.get("/bookstore/v1/product/")

    assert response.status_code == 200
    assert response.data["count"] == 3
    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_create_product_authenticated(api_client):
    category = CategoryFactory()

    payload = {
        "title": "Produto teste",
        "description": "Descrição teste",
        "price": 9990,
        "active": True,
        "category_id": [category.id],
    }

    response = api_client.post(
        "/bookstore/v1/product/",
        payload,
        format="json",
    )

    print("\nERRO DA API:")
    print(response.data)

    assert response.status_code == 201
    assert response.data["title"] == payload["title"]


@pytest.mark.django_db
def test_product_requires_authentication():
    client = APIClient()

    response = client.get("/bookstore/v1/product/")

    assert response.status_code in [401, 403]