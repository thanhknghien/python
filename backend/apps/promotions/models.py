from django.db import models
from apps.books.models import Category

class Promotion(models.Model):
    PromotionID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)
    DiscountPercent = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    StartDate = models.DateField(null=False)
    EndDate = models.DateField(null=False)
    CategoryID = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.Name