from rest_framework import routers
from .views import (
    CategoryViewSet,
    ExpenseViewSet,
    SummaryView,
    LoginView,
    LogoutView,
    SignupView,
    UserInfoView,
    monthlyView,
    amountView,
    categoryView
)
from django.urls import path


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')


urlpatterns = [
    *router.urls,
    path('summary/', SummaryView.as_view(), name='summary'),
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('userinfo/', UserInfoView.as_view(), name='userinfo'), 
    path('monthlyview/',monthlyView.as_view(), name='monthlyView'),
    path("amountview/", amountView.as_view(), name='amountView'),
    path('categoryview/', categoryView.as_view(), name='categoryview')
]