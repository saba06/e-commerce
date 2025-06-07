from django.shortcuts import render,get_object_or_404
from .cart import Cart
from storefront.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    cart_total = cart.get_total()
    return render(request, "cart/cart_summary.html", {
        'cart_products': cart_products, 
        'quantities': quantities,
        "cart_total": cart_total
        })


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, f"Item delete from cart!")
        return response

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        product_id= int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product,id=product_id)
        # save to a session
        cart.add(product=product,quantity=product_qty)
        # get cart quantity
        cart_quantity = cart.__len__()
        # response
        response =  JsonResponse({'qty': cart_quantity})
        messages.success(request, f"{product.name} add to cart!")
        return response
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, f"Cart has been updated")
        return response