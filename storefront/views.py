from django.shortcuts import redirect, render
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def search(request):
    # determined if they have filled out the form
    if request.method == "POST":
        search = request.POST["search"]
        # query the products
        search = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        # if search is null
        if not search:
            messages.success(request, "That product dose not exist!")
            return render(request, 'storefront\search.html', {})
        else:
            return render(request, 'storefront\search.html', {'search': search})
    else:
        return render(request, 'storefront\search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        # get profile
        current_user = Profile.objects.get(user__id=request.user.id)
        # get shipping address
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # get user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # get shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info has been updated!")
            return redirect("home")
        return render(request, "storefront\\update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect("home")


def update_password(request):

    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, "storefront\\update_password.html", {'form':form})
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "storefront\\update_password.html", {'form':form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect("home")

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been updated!")
            return redirect("home")
        return render(request, "storefront\\update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect("home")

def category_summary(request):
    categories = Category.objects.all()
    return render(request, "storefront\category_summary.html", {'categories': categories})

def category(request, foo):
    foo=foo.replace('-', ' ')
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request, 'storefront\category.html',{"products":products,"category":category.name})
    except:
        messages.success(request, "The Catogery Does't Exist..")
        return redirect('home')
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request,"storefront\product.html",{"product":product})

def home(request):
    products = Product.objects.all()
    return render(request, "storefront\home.html", {'products': products})

def about(request):
    return render(request,"storefront\\about.html",{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # retrive old shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                # convert to dictonary using JSON
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictonary to the session
                cart = Cart(request)
                # loop through the cart & add items from database
                for product,quantity in converted_cart.items():
                    cart.db_add(product, quantity)

            messages.success(request, ("You have been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, "))
            return redirect('login')
    else:
        return render(request,"storefront\login.html",{})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out .. "))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("You have Registered Sucessfully!"))
            return redirect('update_info')
        else:
            messages.success(request,('Whoops! There was an Error! Try again!'))
            return redirect('register')
    else:
        return render(request, 'storefront\\register.html', {'form':form})