from django.shortcuts import render
from django.shortcuts import render , redirect
from django.db.models import Count 
from django.views import View
from . models import Product ,Customer , Cart
from . forms import CustomerRegisterationForm , CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request,'app/home.html')

def about(request):
    return render(request,'app/about.html')

def contact(request):
    return render(request,'app/contact.html')

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())


class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',locals())        


class CustomerRegisterationView(View):
    def get(self,request):
        form = CustomerRegisterationForm()
        return render(request, 'app/customerregisteration.html',locals())
    def post(self,request):
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation User Registered Successfully")
        else:
            messages.warning(request,"Invalid User Input")
        return render(request, 'app/customerregisteration.html',locals())


class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirects to the login page

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulation! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")


def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")


def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40    
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_item=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_item:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40    
        return render(request,'app/checkout.html',locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart = Cart.objects.filter(product=prod_id, user=user)
        if cart.exists():
            c = cart.first()  # Retrieve the first Cart object
            c.quantity += 1
            c.save()
        else:
            # Create a new Cart object if it doesn't exist
            c = Cart.objects.create(product=prod_id, user=user, quantity=1)
        
        amount = 0
        for p in Cart.objects.filter(user=user):
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)






def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id', None)
        if not prod_id:
            return JsonResponse({'error': 'Product ID not provided'}, status=400)

        cart_items = Cart.objects.filter(Q(product_id=prod_id) & Q(user=request.user))
        if not cart_items.exists():
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        quantity_removed = sum(item.quantity for item in cart_items)
        cart_items.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        subtotal = sum(item.quantity * item.product.discounted_price for item in cart)
        total_amount = subtotal + 40  # Assuming an additional charge (like shipping)

        data = {
            'quantityRemoved': quantity_removed,  # Optional: Only if you need it on the frontend
            'amount': subtotal,  # Before any additional charges
            'totalamount': total_amount  # Total amount including additional charges
        }

        return JsonResponse(data)

