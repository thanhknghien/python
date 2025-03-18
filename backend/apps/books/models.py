from django.db import models

class Category(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.Name

class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100, null=False)
    Author = models.CharField(max_length=50, null=True)
    Genre = models.CharField(max_length=30, null=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    StockQuantity = models.IntegerField(null=False, default=0)
    CategoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    ImagePath = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.Title