from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nslides), nslides])
    
    params = {'allProds': allProds}
    return render(request, 'index.html', params)


def handlelogin(request):
      if request.method == 'POST':
        loginusername=request.POST['email']
        loginpassword=request.POST['pass1']
        user=authenticate(username=loginusername,password=loginpassword)
       
        if user is not None:
            login(request,user)
            messages.info(request,"Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')    
      return render(request,'login.html')         


def signup(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1 != pass2:

            messages.error(request,"Password do not Match,Please Try Again!")
            return redirect('/signup')
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:            
            pass 
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass        
        user=User.objects.create_user(email,email,pass1)
        user.save()
        messages.info(request,'Thanks For Signing Up')
        return redirect('/login')    
    return render(request,"signup.html")        


def logouts(request):
    logout(request)
    messages.warning(request,"Logout Success")
    return render(request,'login.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('desc')
        mobNo = request.POST.get('mobNo')
        myquery = Contact(name=name, email=email, desc=description, mobNo=mobNo)
        myquery.save()
        messages.info(request, "Applicaton is submitted")
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'prodView.html', {'product':product[0]})


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('/cart/')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        name = request.POST.get('name', '')
        amount = total_price
        email = request.user.email
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        items_description = ", ".join(
            f"{item.product.product_name} x {item.quantity}" for item in cart_items
        )

        order = Orders.objects.create(
            user=request.user,
            items_json=items_description,
            amount=amount,
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            paymentstatus="pending",
            date=timezone.now()
        )

        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been confirmed")
        update.save()

        return render(request, "payment.html", {
            "order": order,
            "amount": order.amount
        })


    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    }) 



def myOrders(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    orders = Orders.objects.filter(user=request.user).order_by('-order_id')

    for order in orders:
        if order.paymentstatus != 'success':
            order.paymentstatus = 'pending'
            order.save()

    return render(request, 'myOrder.html', {'orders': orders})


@login_required(login_url='/auth/login/')
def delete_order(request, order_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    try:
        order = Orders.objects.get(order_id=order_id, user=request.user)
        order.delete()
        messages.success(request, "Order successfully deleted.")
        return redirect('my_order')
    except Orders.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('my_order')



@login_required(login_url='/auth/login/')
def payment(request, order_id):
    try:
        order = Orders.objects.get(order_id=order_id, user=request.user)
        return render(request, 'payment.html', {
            'order': order,
            'amount': order.amount 
        })
    except Orders.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('myOrders')


@csrf_exempt
@login_required(login_url='/auth/login/')
def payment_success(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Orders.objects.get(order_id=order_id, user=request.user)
            order.paymentstatus = 'success'
            order.save()
            Cart.objects.filter(user=request.user).delete()

            return render(request, 'payment_success.html', {'order': order})

        except Orders.DoesNotExist:
            messages.error(request, "Order not found.")
            return redirect('cart:cart_view')
    return render(request, 'payment.html')


@login_required(login_url='/auth/login/')
def user_profile(request):
    user = request.user

    if request.method == "POST":
        new_fName = request.POST.get('first_name')
        new_lName = request.POST.get('last_name')
        new_username = request.POST.get('username')

        user.first_name = new_fName
        user.last_name = new_lName
        user.username = new_username
        user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('/profile')

    return render(request, 'my_profile.html', {'user': request.user})