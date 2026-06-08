from rest_framework.routers import DefaultRouter

from product.viewsets import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register("product", ProductViewSet, basename="product")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = router.urls