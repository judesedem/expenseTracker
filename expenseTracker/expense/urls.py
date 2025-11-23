from rest_framework import routers
from .views import CategoryViewSet,ExpenseViewSet

router= routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns=router.urls