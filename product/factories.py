import factory

from .models import Product, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    slug = factory.Sequence(lambda n: f"category-{n}")
    description = factory.Faker("sentence")
    active = factory.Iterator([True, False])

    class Meta:
        model = Category
        skip_postgeneration_save = True


class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Iterator([10.00, 20.00, 30.00, 40.00, 50.00])
    active = factory.Iterator([True, False])

    class Meta:
        model = Product
        skip_postgeneration_save = True

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)
        else:
            self.category.add(CategoryFactory())