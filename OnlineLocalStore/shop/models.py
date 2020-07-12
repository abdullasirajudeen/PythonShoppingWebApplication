from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class products(models.Model):
	pname = models.CharField(max_length=100)
	ptype = models.CharField(max_length=10)
	description = models.TextField()
	stock = models.IntegerField()
	price  =models.IntegerField()
	img1 = models.ImageField(upload_to='localshop/pics')
	img2 = models.ImageField(upload_to='localshop/pics', default='default.jpg')
	img3 = models.ImageField(upload_to='localshop/pics', default='default.jpg')
	offer = models.BooleanField(default=False)
	isactive = models.BooleanField(default=True) 
	offerprice = models.IntegerField(blank=True,null=True)
	created_at = models.DateField(auto_now_add=True)
	owner = models.ForeignKey(User,default=None,on_delete=models.CASCADE)

	def __str__(self):
		return self.pname
		