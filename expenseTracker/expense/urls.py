from rest_framework import routers
from .views import CategoryViewSet,ExpenseViewSet,UserViewSet

router= routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'User',UserViewSet)
urlpatterns=router.urls