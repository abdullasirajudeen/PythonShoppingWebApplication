from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from localShop.models import userProfile,orderDetails
from .models import products
from django.forms import ModelForm
# Create your views here.
class AddProductForm(ModelForm):
    class Meta:
        model = products
        fields = ['pname','ptype','description', 'stock', 'price', 'img1', 'img2', 'img3', 'offer','offerprice']

class EditProductForm(ModelForm):
    class Meta:
        model = products
        fields = ['pname','ptype','description', 'stock', 'price', 'img1', 'img2', 'img3', 'offer','offerprice','isactive']

def single(request):
	current_user = request.user
	pid = request.GET['id']
	product=products.objects.filter(owner=request.user,id=pid)
	return render(request,"shop/single.html",{'product':product})

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

def neworders(request):
	try:
		orderlist=orderDetails.objects.filter(productid__owner=request.user.id,status=False)
	except orderDetails.DoesNotExist:
		orderlist = None
	return render(request,"shop/orders.html",{'orderlist':orderlist})

def viewproducts(request):
	cid=request.GET['id']
	cuser=User.objects.get(id=cid)
	try:
		orderlist=orderDetails.objects.filter(productid__owner=request.user.id,status=False,userid=cuser)
	except orderDetails.DoesNotExist:
		orderlist = None
	return render(request,"shop/viewproducts.html",{'orderlist':orderlist})

def ordercompleted(request):
	uid = request.GET['id']
	cuser=User.objects.get(id=uid)
	try:
		orderlist=orderDetails.objects.get(productid__owner=request.user.id,status=False,userid=cuser)
	except orderlist.DoesNotExist:
		orderlist = None
	if orderlist:
		orderlist.status = True
		orderlist.save()
		return redirect('/shop/neworders')
	else:
		print('Something went wrong, TryAgain')
		return redirect('/shop/neworders')

def editproduct(request):
	pid = request.GET['id']
	if request.method == 'POST':
		current=products.objects.get(id=pid)
		form = EditProductForm(request.POST,request.FILES or None,instance=current)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			return redirect(r'/shop/single?id='+pid)
		else:
			form = EditProductForm(request.POST,request.FILES or None)
			context={
			'form':form
			}
			return render(request,"shop/addproduct.html",context)
	else :
		current_user = request.user
		product=products.objects.filter(owner=request.user,id=pid)
		for pro in product:
			form = EditProductForm(initial={'pname': pro.pname,'ptype': pro.ptype,'description': pro.description,'stock': pro.stock,'isactive':pro.isactive,'price': pro.price,'img1': pro.img1,'img2': pro.img2,'img3': pro.img3,'offer': pro.offer,'offerprice': pro.offerprice,'isactive':pro.isactive})
			context={
			'form':form
			}
		return render(request,"shop/addproduct.html",context)

def marksold(request):
	pid = request.GET['id']
	try:
		product=products.objects.get(owner=request.user,id=pid)
	except products.DoesNotExist:
		product = None
	if product:
		product.isactive = False
		product.save()
		return redirect('/shop/index')
	else:
		print('Something went wrong, TryAgain')
		return redirect('/shop/index')

def deleteproduct(request):
	pid = request.GET['id']
	try:
		product=products.objects.get(owner=request.user,id=pid)
	except products.DoesNotExist:
		product = None
	if product:
		product.delete()
		return redirect('/shop/index')
	else:
		print('Something went wrong, TryAgain')
		return redirect('/shop/index')