from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver



class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    imagePath = models.ImageField(upload_to='book_images', null=True, blank=True, default='book_images/default.png')
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ], default='available')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ], default='Pending')
    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)\
    
    def get_total(self):
        return self.total_amount

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"

class StockIn(models.Model):
    price = models.FloatField(default=0)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"StockIn {self.book.title} - {self.quantity}"

@receiver(post_save, sender=StockIn)
def update_book_stock(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        book.stock += instance.quantity
        book.save()

class StockOut(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"StockOut {self.book.title} - {self.quantity}"

@receiver(post_save, sender=StockOut)
def update_book_stock_out(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        book.stock -= instance.quantity
        if book.stock < 0:
            raise ValueError(f"Stock for book {book.title} cannot be negative.")
        book.save()

@receiver(pre_save, sender=Order)
def create_stock_out_on_order_confirmed(sender, instance, **kwargs):
    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        old_order = None

    if old_order and old_order.status != "Confirmed" and instance.status == "Confirmed":
        order_details = OrderDetail.objects.filter(order=instance)
        for detail in order_details:
            if detail.book.stock < detail.quantity:
                raise ValueError(f"Not enough stock for book {detail.book.title}. Required: {detail.quantity}, Available: {detail.book.stock}")
            StockOut.objects.create(
                order=instance,
                book=detail.book,
                quantity=detail.quantity,
                note=f"Auto-generated for Order {instance.id} on confirmation"
            )

class Report_Revenue(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Report Revenue'
        verbose_name_plural = 'Report Revenue'
        
    def __str__(self):
        return 'Report Revenue'

class Report_Inventory(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Report Inventory'
        verbose_name_plural = 'Report Inventory'
        
    def __str__(self):
        return 'Report Inventory'
