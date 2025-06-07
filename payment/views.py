import datetime
from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from storefront.models import Product, Profile

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            order = Order.objects.filter(id=pk)
            status = request.POST['shipping_status']
            # check if true or false
            if status == "true":
                order.update(shipped=True,date_shipped=datetime.datetime.now())
            else:
                order.update(shipped=False)
            messages.success(request, "Shipping status updated!")
            return redirect('home')
        
        return render(request, 'payment/orders.html', { 'order': order, 'items': items })
    else:
        messages.success(request, "Access Denied!")
        return redirect("home")


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=True,date_shipped=datetime.datetime.now())
            messages.success(request, "Shipping status updated!")
        
        return render(request,'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect("home")

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            messages.success(request, "Shipping status updated!")
        
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect("home")
    
def process_order(request):
    if request.POST:

        # get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        cart_total = cart.get_total()

        # get billing info from last page
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        # gather order info
        full_name = my_shipping["shipping_full_name"]
        email = my_shipping["shipping_email"]
        # create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid =  cart_total

        if request.user.is_authenticated:
            # logged in 
            user = request.user
            # create order
            create_order = Order(user=user, full_name=full_name,email=email,shipping_address=shipping_address, amount_paid=amount_paid) 
            create_order.save()
            # add order items
            for product in cart_products:
                product_id = product.pk
                if product.on_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                # get quantity
                create_order_item = OrderItem(
                    order=create_order, Product=product, user=user, quantity=quantities[str(product_id)], price=product_price)
                create_order_item.save()
            # delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            # delete cart from db 
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")
            
            messages.success(request, "Order placed!")
            return redirect('home')
        else:
            # logged out
            create_order = Order(full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            # add order items
            for product in cart_products:
                product_id = product.pk
                if product.on_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                # get quantity
                create_order_item = OrderItem(
                    order=create_order, Product=product, quantity=quantities[str(product_id)], price=product_price)
                create_order_item.save()
            # delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            messages.success(request, "Order placed!")
            return redirect('home')
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')
    
def billing_info(request):
    if request.POST:

        # get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        cart_total = cart.get_total()
        # get shipping form
        shipping_info = request.POST

        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        # is use logged in
        if request.user.is_authenticated:
            # get the billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                'cart_products': cart_products,
                'quantities': quantities,
                "cart_total": cart_total,
                "shipping_info": shipping_info,
                "billing_form": billing_form
            })
        else:
            # not logged in 
            # get the billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                'cart_products': cart_products,
                'quantities': quantities,
                "cart_total": cart_total,
                "shipping_info": shipping_info,
                "billing_form": billing_form
            })
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')
    
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    cart_total = cart.get_total()
    
    if request.user.is_authenticated:
        # get shipping address
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # get shipping form
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
        # checkout as user
        return render(request, "payment/checkout.html", {
            'cart_products': cart_products, 
            'quantities': quantities,
            "cart_total": cart_total,
            "shipping_form":shipping_form
            })
    else:
        # get shipping form
        shipping_form = ShippingForm(
            request.POST or None)
        # checkout as guest
        return render(request, "payment/checkout.html", {
            'cart_products': cart_products, 
            'quantities': quantities,
            "cart_total": cart_total,
            "shipping_form": shipping_form
            })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})