from rest_framework import serializers
from .models import Category,Expense
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields=['username','id','email','password']
       
    def create(self,validated_data):
        user=User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email exists")
        return value