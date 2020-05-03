from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from localShop.models import userProfile
from .models import products
from django.forms import ModelForm
# Create your views here.
class AddProductForm(ModelForm):
    class Meta:
        model = products
        fields = ['pname','ptype','description', 'stock', 'price', 'img1', 'img2', 'img3', 'offer','offerprice']

def addproduct(request):
	current_user = request.user
	form = AddProductForm(request.POST,request.FILES or None)
	context={
		'form':form
		}
	if request.method == 'POST':
		
		if form.is_valid():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			return redirect(r'/shop/index')
		else:
			form = AddProductForm(request.POST or None)
			context={
			'form':form
			}
			return render(request,"shop/addproduct.html",context)
	else :
		form = AddProductForm()
		context={
		'form':form
		}
		return render(request,"shop/addproduct.html",context)


def login(request):
	if request.method == 'POST':
		password=request.POST['password']
		username=request.POST['username']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			if user.userprofile.is_store:
				auth.login(request,user)
				return redirect('/shop/index')
			else :
				return redirect('/shop/login')
		else :
			return redirect('/shop/login')
	else:
		return render(request,"shop/login.html")

def signup(request):
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
			return redirect('/shop/login')
		except Exception as e:
			print(e)
			print('something wrong')
			return render(request,"shop/singup.html")
	else:
		return render(request,"shop/singup.html")

def logout(request):
	auth.logout(request)
	return redirect('/')

def index(request):
	current_user = request.user
	product=products.objects.filter(owner=request.user)
	return render(request,"shop/index.html",{'product':product})#temporary