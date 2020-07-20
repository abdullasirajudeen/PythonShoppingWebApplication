from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import userProfile, cart, orderDetails, check_product_stock, reviewDetails
from shop.models import products
from django.db import transaction
from django.db.models import F
import urllib
from django.http import HttpResponse

# Create your views here.
from django.http import JsonResponse

def autocomplete(request):
    if request.is_ajax():
        queryset = products.objects.filter(pname__icontains=request.GET.get('search', None),isactive=True)
        list = []        
        for i in queryset:
            list.append(i.pname)
        data = {
            'list': list,
        }
        return JsonResponse(data)

def index(request):
	return render(request,"localshop/index.html")

def addreview(request):
	if request.user.is_anonymous:
		return redirect('/')
	pid = request.GET['id']
	star = request.GET['star']
	review = request.GET['review']
	product=products.objects.get(id=pid)
	try:
		chkreview=reviewDetails.objects.get(userid=request.user,productid=product)
	except reviewDetails.DoesNotExist:
		chkreview = None
	if chkreview:
		chkreview.stars=star
		chkreview.review=review
		chkreview.save()
		return HttpResponse('Review Updated')
	else:
		instance=reviewDetails(userid=request.user,productid=product,stars=int(star),review=review)
		instance.save()
		return HttpResponse('Review Added')
	
	return HttpResponse('Something went wrong, TryAgain')

def login(request):
	if request.method == 'POST':
		password=request.POST['password']
		username=request.POST['username']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else :
			return render(request,"localshop/index.html",{"logmsg":"Incorrect username or Password..Try Again..!"})
	else:
		return render(request,"localshop/index.html")

def logout(request):
	auth.logout(request)
	return redirect('/')

def search(request):
	try:
		name=request.GET['pname']
	except:
		name = ""	
	trate=3
	try:
		product=products.objects.filter(isactive=True,pname__startswith=name)
	except:
		product=None
	return render(request,"localshop/search.html",{'product':product})

def checkout(request):
	if request.user.is_anonymous:
		return redirect('/')
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
	if request.user.is_anonymous:
		return redirect('/')
	user = request.user
	paymode=request.POST['optradio']
	flag=False
	address=user.first_name+user.last_name+","+user.userprofile.house+","+user.userprofile.town+","+user.userprofile.state+","+str(user.userprofile.pincode)+","+str(user.userprofile.phone)+","+user.email
	print(paymode)
	try:
		cartlist=cart.objects.filter(userid=request.user.id)
	except cart.DoesNotExist:
		cartlist = None
	if cartlist:
		with transaction.atomic():	
			for item in cartlist:
				product=products.objects.get(id=item.productid.id)
				instance = orderDetails(userid=request.user,productid=product,quantity=item.quantity,address=address,paymode=paymode)
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
	if request.user.is_anonymous:
		return redirect('/')
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
	if request.user.is_anonymous:
		return redirect('/')
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
	if request.user.is_anonymous:
		return redirect('/')
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

def shopsnearme(request):
	if request.user.is_anonymous:
		return redirect('/')
	try:
		cat = request.GET['cat']
	except:
		cat = 'All'	
	trate=3
	try:
		shops=User.objects.filter(userprofile__is_store=True)
	except:
		shops=None
	return render(request,"localshop/shopsnearme.html",{'product':shops})

def shopproducts(request):
	try:
		sid = request.GET['id']
	except:
		print("no id got as parameter")
	try:
		shop=User.objects.get(id=sid)
		product=products.objects.filter(isactive=True,owner=shop)
	except:
		product=None
	return render(request,"localshop/shopproducts.html",{'product':product})

def signup(request):
	if request.method == 'POST':
		first_name=request.POST['firstname']
		last_name=request.POST['lastname']
		email=request.POST['email']
		password=request.POST['password']
		username=request.POST['email']
		phone=request.POST['phone']
		address=request.POST['address']
		town=request.POST['town']
		state=request.POST['state']
		pincode=request.POST['pincode']
		try:
			user =User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
			profile=userProfile(user=user,state=state,town=town,address=address,pincode=pincode,phone=phone)
			user.save();
			profile.save();
			print('created')
			return redirect('/')
		except Exception as e:
			print(e)
			if str(e)[0:44]=="UNIQUE constraint failed: auth_user.username":
				msg="Email Already Taken.Try Different One..!"
			else:
				msg="Something went wrong, Try Again..."
			return render(request,"localshop/singup.html",{'status':True,'msg':msg})
	else:
		return render(request,"localshop/singup.html")

def orderhistory(request):
	if request.user.is_anonymous:
		return redirect('/')
	try:
		orderlist=orderDetails.objects.filter(userid_id=request.user,status=True)
	except orderlist.DoesNotExist:
		orderlist = None
	return render(request,"localshop/orderhistory.html",{'orderlist':orderlist})

def single(request):
	pid = request.GET['id']
	product=products.objects.filter(id=pid)
	tstar=0
	soldcount=0
	buyed=False
	if not request.user.is_anonymous:
		try:
			orderlist=orderDetails.objects.filter(userid_id=request.user,status=True,productid_id=pid)
		except orderDetails.DoesNotExist:
			orderlist=None
		if orderlist:
			buyed=True
	try:
		chkreview=reviewDetails.objects.filter(productid=pid)
		for rev in chkreview:
			tstar+=rev.stars
	except reviewDetails.DoesNotExist:
		chkreview = None

	return render(request,"localshop/single.html",{'product':product,'buyed':buyed,'chkreview':chkreview})
