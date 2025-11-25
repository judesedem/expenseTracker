from rest_framework import routers
from .views import CategoryViewSet,ExpenseViewSet,UserViewSet,SummaryView
from django.urls import path


router= routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'User',UserViewSet)



urlpatterns=[
    *router.urls,
    path('summary',SummaryView.as_view(), name='summary'),
             
]
