from django.db import models


# Create your models here.
class Medicine(models.Model):
    Name = models.CharField(max_length=100,unique=True,blank=True)
    Type = models.CharField(max_length=100,blank=True)
    Price = models.IntegerField()
    Manufacturing_date = models.DateField(blank=True)
    Expiry_date = models.DateField()
    
    def __str__(self):
        return self.Name
    
          