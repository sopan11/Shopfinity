from django.shortcuts import render, redirect
from django.contrib import messages
from .models import adminUser
from ecommerceapp.models import Product
from math import ceil
from django.shortcuts import get_object_or_404
from ecommerceapp.models import Orders, OrderUpdate
from datetime import date

# Create your views here.
def login_ad(request):
    if request.method=="POST":
        username = request.POST['email']
        user_password = request.POST['pass1']

        try:
            admin = adminUser.objects.get(email=username)
        except adminUser.DoesNotExist:
            messages.error(request, "Admin with this email does not exist")
            return redirect('/shopfinity/adm-user/login')

        if admin.password == user_password:
            request.session['admin_id'] = admin.id
            request.session['admin_email'] = admin.email
            messages.success(request, "Admin login successful")
            return redirect('/shopfinity/adm/all-products') 
        else:
            messages.error(request, "Incorrect password")
            return redirect('/shopfinity/adm-user/login')
        
    return render(request, 'admins/admin_login.html')


def add_products(request):
    if not request.session.get('admin_id'):
        messages.error(request, "Please login as admin to add products.")
        return redirect('/shopfinity/adm-user/login')

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')

        product = Product(
            product_name=product_name,
            category=category,
            sub_category=sub_category,
            price=price,
            desc=desc,
            image=image
        )
        product.save()
        messages.success(request, "Product added successfully!")
        return redirect('/shopfinity/adm/add-product')  # Change if needed

    return render(request, 'admins/addProducts.html')


def all_products(request):
    if not request.session.get('admin_id'):
        messages.error(request, "Please login as admin to add products.")
        return redirect('/shopfinity/adm-user/login')

    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        allProds.append([prod, range(1)])
    
    params = {'allProds': allProds}
    return render(request, 'admins/allProducts.html', params)


def delete_product(request, product_id):
    if not request.session.get('admin_id'):
        messages.error(request, "Please login as admin to delete products.")
        return redirect('/shopfinity/adm-user/login')

    product = get_object_or_404(Product, id=product_id)
    
    try:
        product.delete()
        messages.success(request, f"Product '{product.product_name}' deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting product: {str(e)}")

    return redirect('/shopfinity/adm/all-products')


def update_product(request, product_id):
    if not request.session.get('admin_id'):
        messages.error(request, "Please login as admin to update products.")
        return redirect('/shopfinity/adm-user/login')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.category = request.POST.get('category')
        product.sub_category = request.POST.get('sub_category')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect('/shopfinity/adm/all-products')

    return render(request, 'admins/updateProduct.html', {'product': product})



def admin_all_orders(request):
    if not request.session.get('admin_id'):
        messages.error(request, "Please login as admin to update products.")
        return redirect('/shopfinity/adm-user/login')

    orders = Orders.objects.filter(paymentstatus='success').order_by('-date')
    updates = OrderUpdate.objects.all()

    updates_map = {}
    for update in updates:
        updates_map.setdefault(update.order_id, []).append(update)

    combined_data = []
    for order in orders:
        combined_data.append({
            'order': order,
            'updates': updates_map.get(order.order_id, [])
        })

    return render(request, 'admins/allOrders.html', {
        'combined_data': combined_data
    })



    
def mark_order_delivered(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Orders, order_id=order_id)
        order.orderStatus = 'Delivered'
        print(order_id)
        oid = order.oid
        print(oid)
        order.save()

        orderupdate = OrderUpdate.objects.get(order_id = order_id)
        orderupdate.new_update_desc += f"Order delivered ({date.today().strftime('%B %d, %Y')})"
        orderupdate.delivered = True
        orderupdate.save()

        messages.success(request, f"Order #{order_id} marked as delivered.")
    return redirect('admin_all_orders')