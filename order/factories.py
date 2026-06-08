import factory

from django.contrib.auth.models import User
from product.factories import ProductFactory

from .models import Order


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)