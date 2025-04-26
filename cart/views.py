from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import Product
from .models import Cart
from django.http import JsonResponse
from django.contrib import messages


@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return render(request, 'authentication/login.html')
    
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)  
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

            if not created:
                cart_item.quantity += 1 
            cart_item.save()

            return JsonResponse({'message': 'Product added to cart successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_view')


@login_required
def update_cart(request, product_id, quantity):
    try:
        cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_view')

