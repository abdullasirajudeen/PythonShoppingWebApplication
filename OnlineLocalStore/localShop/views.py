from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import userProfile, cart, orderDetails, check_product_stock
from shop.models import products
from django.db import transaction
from django.db.models import F
import urllib
from django.http import HttpResponse

# Create your views here.

def index(request):
	return render(request,"localshop/index.html")

def login(request):
	if request.method == 'POST':
		password=request.POST['password']
		username=request.POST['username']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else :
			return redirect('/login')
	else:
		return render(request,"localshop/index.html")

def logout(request):
	auth.logout(request)
	return redirect('/')

def search(request):
	try:
		cat = request.GET['cat']
	except:
		cat = 'All'	
	trate=3
	product=products.objects.filter(isactive=True)
	return render(request,"localshop/search.html",{'product':product})

def checkout(request):
	try:
		cartlist=cart.objects.filter(userid=request.user.id)
	except cart.DoesNotExist:
		cartlist = None
	total=0
	subtotal=[]
	if cartlist:
		for item in cartlist:
			if item.productid.offer:
				subtotal.append(item.productid.offerprice*item.quantity)
				total=total+item.productid.offerprice*item.quantity
			else:
				subtotal.append(item.productid.price*item.quantity)
				total=total+item.productid.price*item.quantity
	return render(request,"localshop/checkout.html",{'product':cartlist,'subtotal':subtotal,'total':total})

def orderstatus(request):
	user = request.user
	#paymode=request.POST['optradio']
	flag=False
	address=user.first_name+user.last_name+","+user.userprofile.house+","+user.userprofile.town+","+user.userprofile.state+","+str(user.userprofile.pincode)+","+str(user.userprofile.phone)+","+user.email
	print(address)
	try:
		cartlist=cart.objects.filter(userid=request.user.id)
	except cart.DoesNotExist:
		cartlist = None
	if cartlist:
		with transaction.atomic():	
			for item in cartlist:
				product=products.objects.get(id=item.productid.id)
				instance = orderDetails(userid=request.user,productid=product,quantity=item.quantity,address=address,paymode="paymode")
				product.stock = F('stock')- item.quantity
				try:
					product.save()
					check_product_stock(product.id)
					instance.save()
					print("added to o list")
					#return HttpResponse('Added to Cart')
				except Exception as e:
					print(e)
					print("Something went wrong with ol, TryAgain")
					#return HttpResponse('Something went wrong, TryAgain')
			flag=True

	try:
		cartlist=cart.objects.filter(userid=request.user.id)
	except cart.DoesNotExist:
		cartlist = None
	if cartlist:
		with transaction.atomic():	
			for item in cartlist:
				try:
					item.delete()
					print("deleted from cart")
					#return HttpResponse('Added to Cart')
				except Exception as e:
					print(e)
					print("Something went wrong, TryAgain")
					#return HttpResponse('Something went wrong, TryAgain')
			flag=True

	if flag:
		return render(request,"localshop/order_status.html",{'status':flag})

def viewcart(request):
	try:
		cartlist=cart.objects.filter(userid=request.user.id)
	except cart.DoesNotExist:
		cartlist = None
	total=0
	subtotal=[]
	if cartlist:
		for item in cartlist:
			if item.productid.offer:
				subtotal.append(item.productid.offerprice*item.quantity)
				total=total+item.productid.offerprice*item.quantity
			else:
				subtotal.append(item.productid.price*item.quantity)
				total=total+item.productid.price*item.quantity
	return render(request,"localshop/cart.html",{'cartlist':cartlist,'subtotal':subtotal,'total':total})



def removefromcart(request):
	
	pid = request.GET['id']
	product=products.objects.get(id=pid)
	try:
		chkcart=cart.objects.get(productid=pid,userid=request.user.id)
	except cart.DoesNotExist:
		chkcart = None
	if chkcart:
		try:
			chkcart.delete()
			return HttpResponse('Product Removed from Cart')
		except:
			return HttpResponse('Something went wrong, TryAgain')
	else:
		return HttpResponse('No such Product in Cart')

def addtocart(request):
	
	pid = request.GET['id']
	qty = request.GET['qty']
	product=products.objects.get(id=pid)
	try:
		chkcart=cart.objects.get(productid=pid,userid=request.user.id)
	except cart.DoesNotExist:
		chkcart = None
	if chkcart:
		return HttpResponse('Product already in Cart')
	else:
		instance = cart(userid=request.user,productid=product,quantity=qty)
		try:
			instance.save()
			return HttpResponse('Added to Cart')
		except:
			return HttpResponse('Something went wrong, TryAgain')
