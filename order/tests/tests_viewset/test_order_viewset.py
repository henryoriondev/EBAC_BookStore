import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from order.models import Order
from product.factories import ProductFactory


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
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    return client


@pytest.mark.django_db
def test_list_orders_authenticated(api_client, user):
    product = ProductFactory()

    order = Order.objects.create(user=user)
    order.product.add(product)

    response = api_client.get("/bookstore/v1/order/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_create_order_authenticated(api_client, user):
    product = ProductFactory()

    payload = {
        "user": user.id,
        "product_id": [product.id],
    }

    response = api_client.post(
        "/bookstore/v1/order/",
        payload,
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_order_requires_authentication():
    client = APIClient()

    response = client.get("/bookstore/v1/order/")

    assert response.status_code in [401, 403]