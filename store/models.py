from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    # for example below is 9999.99
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    Collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion,related_name='products')


class Customer(models.Model):

    MEMBERSHIP_BORONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOISES=[
        (MEMBERSHIP_BORONZE,'BORONZE'),
        (MEMBERSHIP_SILVER,'SILVER'),
        (MEMBERSHIP_GOLD,'GOLD')
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership= models.CharField(max_length=1,choices=MEMBERSHIP_CHOISES,default=MEMBERSHIP_BORONZE)

class Order(models.Model):
    PAYMENT_STATE_PENDEING = 'P'
    PAYMENT_STATE_COMPLATE = 'C'
    PAYMENT_STATE_FAILED = 'F'

    PAYMENT_STATE_CHOISES = [
        (PAYMENT_STATE_PENDEING,'PENDING'),
        (PAYMENT_STATE_COMPLATE,'COMPLATE'),
        (PAYMENT_STATE_FAILED,'FAILED')
    ]
    place_at = models.DateTimeField(auto_now_add=True)
    payment_state = models.CharField(max_length=1,choices=PAYMENT_STATE_CHOISES,default=PAYMENT_STATE_PENDEING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    Product=models.ForeignKey(Product,on_delete=models.PROTECT)

    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()






class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)




