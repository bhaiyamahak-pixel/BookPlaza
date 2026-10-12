from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('self_help', 'Self Help'),
        ('biography', 'Biography'),
        ('children', 'Children'),
        ('technology', 'Technology'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='books/')
    stock = models.IntegerField(default=1)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fiction')

    def __str__(self):
        return self.title
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"BP{self.id} - {self.customer_name}"

    def __str__(self):
        return self.customer_name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class CartOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.book.title
        
class CartItem(models.Model):     
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)

     def __str__(self):
        return f"{self.customer.name} - {self.book.title}"