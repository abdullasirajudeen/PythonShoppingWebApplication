from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import userProfile

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

	#current_user = request.user
	#product=products.objects.filter(isactive=True)
	#return render(request,"public/shop.html",{'product':product,'cat':cat})
	return render(request,"localshop/search.html",{'trate':trate})

def slogin(request):
	if request.method == 'POST':
		password=request.POST['password']
		username=request.POST['username']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			if user.userprofile.is_store:
				auth.login(request,user)
				return redirect('/storeindex')
			else :
				return redirect('/slogin')
		else :
			return redirect('/slogin')
	else:
		return render(request,"localshop/slogin.html")

def ssignup(request):
	if request.method == 'POST':
		first_name=request.POST['firstname']
		last_name=request.POST['lastname']
		email=request.POST['email']
		password=request.POST['password']
		username=request.POST['email']
		shopname=request.POST['shopname']
		phone=request.POST['phone']
		description=request.POST['description']
		address=request.POST['address']
		town=request.POST['town']
		state=request.POST['state']
		pincode=request.POST['pincode']
		shopimage=request.FILES['shopimage']
		license=request.POST['license']
		try:
			user =User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
			user.save();
			profile=userProfile(user=user,state=state,shop_name=shopname,town=town,address=address,pincode=pincode,phone=phone,is_store=True,description=description,img=shopimage,license_no=license)
			profile.save();
			print('created')
			return redirect('/slogin')
		except Exception as e:
			print(e)
			print('something wrong')
			return render(request,"localshop/ssingup.html")
	else:
		return render(request,"localshop/ssingup.html")

def storeindex(request):
	return render(request,"localshop/base.html")#temporary