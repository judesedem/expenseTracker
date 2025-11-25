from rest_framework import viewsets
import logging
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
logger=logging.getLogger('expense')
from .models import Category,Expense
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer,ExpenseSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated



class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category','amount']

    def create(self,request,*args,**kwargs):
        try:
            response=super().create(request,*args,**kwargs)
            logger.info(f"Expense created by user {request.user}")
            return response
        except Exception as e:
            logger.error(f"Error creating expense:{str(e)}")
            return Response({"error": "Failed to create expense"},status=400)
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now()
        current_year = today.year
        current_month = today.month

        # Monthly total
        monthly_total = Expense.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0

     
        yearly_total = Expense.objects.filter(
            user=user,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "month": today.strftime("%B %Y"),
            "monthly_spent": monthly_total,
            "year": current_year,
            "yearly_spent": yearly_total,
            "currency": "USD",
            "message": f"Hello {user.username}! Here's your summary"
        })
    
#User registration
#pagination and filtering and input validation
#Creating monthly and yearly summary
#Logging and error handling