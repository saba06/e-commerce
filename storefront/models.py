import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# create a user profile upon register
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# automate the profile saving
post_save.connect(create_profile,sender=User)

# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str_(self):
        return f"name={self.name}"

    class Meta:
        verbose_name_plural = 'categories'

class Product(models.Model):    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default="", blank=True)
    image = models.ImageField(upload_to='uploads/product')
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str_(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity =  models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=50,default="",blank=True)
    phone = models.CharField(max_length=20,default="", blank=True)
    date = models.DateField(default=datetime.datetime.today) 
    status = models.BooleanField(default=False)

    def __str_(self):
        return f"product={self.product.id},customer={self.customer.id},quantity={self.quantity},address={self.address},phone={self.phone},date={self.date},status={self.status}"
