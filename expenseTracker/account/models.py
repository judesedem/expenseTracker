from django.db import models

class User(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    CATEGORY_CHOICES={
        'G':'General',
        'F':'Food',
        'H':'Health',
        'E':'Education',
        'B':'Bills'
    }
    category=models.CharField(max_length=1,choices=CATEGORY_CHOICES)
    start_date=models.DateField()
    end_date=models.DateField(auto_now=True)
# Create your models here.
