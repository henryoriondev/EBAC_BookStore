import pytest

from order.factories import OrderFactory
from product.factories import ProductFactory
from order.serializers import OrderSerializer


@pytest.mark.django_db
def test_order_serializer_total():
    product_1 = ProductFactory(price=10)
    product_2 = ProductFactory(price=20)

    order = OrderFactory(product=[product_1, product_2])

    serializer = OrderSerializer(order)

    assert serializer.data["total"] == 30