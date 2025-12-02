from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.views import APIView
from django.utils import timezone
import logging

logger = logging.getLogger('expense')

from .models import Category, Expense
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, ExpenseSerializer, SignupSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()             
            token = Token.objects.create(user=user)
            return Response({
                "token": token.key, 
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key, 
                "user": {"username": user.username, "email": user.email},
                "message": "Successfully logged in"
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):        
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Category created by user {request.user}")
            return response
        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            return Response({"error": "Failed to create category"}, status=status.HTTP_400_BAD_REQUEST)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'amount']

    def get_queryset(self):
        # CRITICAL: Only return expenses for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user when creating an expense
        serializer.save(user=self.request.user)
        logger.info(f"Expense created by user {self.request.user}")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating expense: {str(e)}")
            return Response({"error": "Failed to create expense"}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "id": request.user.id
        })

class monthlyView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        month=request.query_params.get('month')
        year=request.query_params.get('year')
        expense=Expense.objects.filter(user=request.user, date__month=month,date__year=year)
        serializer=ExpenseSerializer(expense,many=True)
        return Response(serializer.data)
 
class amountView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        start=request.query_params.get('start')
        end=request.query_params.get('end')
        amount=Expense.objects.filter(user=request.user,amount__gte=start, amount__lte=end)
        serializer=ExpenseSerializer(amount, many=True)
        return Response(serializer.data)
    
class categoryView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        category=request.query_params.get('category')
        expense=Expense.objects.filter(user=request.user, category__name=category)
        serializer=ExpenseSerializer(expense,many=True)
        return Response(serializer.data)
    
    
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user        
        current_year = request.query_params.get('year')
        current_month = request.query_params.get('month')

        # Monthly total - ONLY for this user
        monthly_total = Expense.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Yearly total - ONLY for this user
        yearly_total = Expense.objects.filter(
            user=user,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({            
            "monthly_spent": monthly_total,
            "year": current_year,
            "yearly_spent": yearly_total,
            "currency": "USD",
            "message": f"Hello {user.username}! Here's your summary"
        })
    

    