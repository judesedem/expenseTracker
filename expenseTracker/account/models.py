from django.db import models

class User(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    CATEGORY_CHOICES=[
        ('G','General'),
        ('F','Food'),
        ('H','Health'),
        ('E','Education'),
        ('B','Bills')
    
    ]
      
    category=models.CharField(max_length=1,choices=CATEGORY_CHOICES,default='G')
    amount=models.DecimalField(max_length=10,decimal_places=2)
    start_date=models.DateField()
    end_date=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}-{self.get_category()}"
    
    

