from rest_framework import viewsets
from .models import Category,Expense
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer,ExpenseSerializer,UserSerializer
from django.contrib.auth.models import User

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category','amount']
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
#User registration
#pagination and filtering and input validation
#Creating monthly and yearly summary
#Logging and error handling