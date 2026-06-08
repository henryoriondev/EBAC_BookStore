import factory

from .models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):

    title = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('sentence')
    active = factory.Iterator([True, False])
    
    class Meta:
        model = Category
        skip_postgeneration_save = True
        
        
class ProductFactory(factory.django.DjangoModelFactory):

    price = factory.Faker('pydecimal')
    category = factory.LazyAttribute(CategoryFactory)
    title = factory.Faker('word')
    
    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)
    class Meta:
        model = Product
        skip_postgeneration_save = True