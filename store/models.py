from django.db import models
from django.core.validators import MinValueValidator


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    #featured_product = models.ForeignKey('Product', on_delete= models.CASCADE, related_name= '+')
    def __str__(self) -> str:
        return self.title
    

class Product(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES =[
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1,message="hi")])
    
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE )
    collection = models.ForeignKey(Collection , on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, related_name='products' )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    
    def __str__(self) -> str:
        return self.first_name
    

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product , on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, null=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
