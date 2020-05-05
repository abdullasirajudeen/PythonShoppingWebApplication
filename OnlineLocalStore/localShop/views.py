from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import userProfile
from shop.models import products

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

