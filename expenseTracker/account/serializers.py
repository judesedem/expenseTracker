from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","category","start_date","end_date"]