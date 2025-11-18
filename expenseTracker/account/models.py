from django.db import models
from django.contrib.auth.models import User

class Expenses(models.Model):    
    CATEGORY_CHOICES=[
        ('G','General'),
        ('F','Food'),
        ('H','Health'),
        ('E','Education'),
        ('B','Bills')
    
    ]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.CharField(max_length=1,choices=CATEGORY_CHOICES,default='G')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    start_date=models.DateField()
    end_date=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -{self.amount}-{self.get_category_display()}"
    
    

