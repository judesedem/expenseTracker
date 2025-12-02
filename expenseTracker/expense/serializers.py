from rest_framework import serializers
from .models import Category, Expense 
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'notes', 'user']
        read_only_fields = ['user']  # User is auto-assigned, not manually set


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, min_length=3)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)  # Fixed: min_length, not max_length

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username or password")
        
        attrs['user'] = user
        return attrs
    
# class ExpenseList(generics.ListAPIView):
    
#     serializer_class = ExpensesSerializer
#     filterset_class = ExpensesFilter
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
        
#         return Expenses.objects.filter(user=self.request.user)
    