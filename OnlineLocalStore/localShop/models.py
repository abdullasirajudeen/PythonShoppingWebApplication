from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from shop.models import products
# Create your models here.

class userProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	state = models.CharField(max_length=200,default='')
	shop_name = models.CharField(max_length=200,default='')
	house = models.CharField(max_length=200,default='')
	town = models.CharField(max_length=200,default='')
	address = models.CharField(max_length=200,default='')
	pincode = models.CharField(max_length=12,default='')
	phone = models.CharField(max_length=12,default='')
	is_store = models.BooleanField(default=False)
	description = models.CharField(max_length=200,default='')
	img = models.ImageField(upload_to='localshop/pics', default='default.jpg')
	is_active = models.BooleanField(default=True)
	license_no = models.CharField(max_length=20,default='')
	
def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile=userProfile.objects.create(user=kwargs['instance'])

def check_product_stock(pid):
	product=products.objects.get(id=pid)
	if product.stock==0:
		product.isactive=False
		product.save()
		print("marked inactive")
		
class orderDetails(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	productid = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	date = models.DateTimeField(auto_now_add=True)
	address = models.TextField()
	status = models.BooleanField(default=False)
	paymode = models.CharField(max_length=20,default=None)
	
class cart(models.Model):
	userid = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	productid = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
