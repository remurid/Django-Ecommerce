from django.shortcuts import get_object_or_404, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from store.models import Product, Category, Order, Orderitem
from .models import Userprofile
# Create your views here.

@login_required
def add_product(request):
    if request.method == 'POST':
        
        user = request.user
        category = request.POST["category"]
        title = request.POST["name"]
        slug = slugify(title)
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.FILES["img_input"]
        categoryData = Category.objects.get(slug=category)
        newProduct = Product(
            user=user,
            category =categoryData,
            title =title,
            slug=slug,
            description=description,
            price=price,
            image=image
        )
        
        newProduct.save()
        return HttpResponseRedirect(reverse("vendor_products"))
        

    
    categories=Category.objects.all()

    return render(request, 'userprofile/add_product.html', {
        'categories':categories
    })

@login_required
def vendors_orders(request):
    orders_items = Orderitem.objects.filter(product__user=request.user)
    
    return render(request, 'userprofile/vendor_orders.html', {
        'order_items':orders_items
    })

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    products = request.user.products.exclude(status=Product.DELETED)
    if request.method == 'POST':
        title = request.POST["name"] 
        product.user = request.user
        category1 = request.POST["category"]
        product.title = request.POST["name"]
        product.slug = slugify(title)
        product.description = request.POST["description"]
        product.price = request.POST["price"]
        image = request.FILES.get("img_input")
        if image:
            product.image = image
        categoryData  = Category.objects.get(slug=category1)
        product.category= categoryData
        product.save()
        categories=Category.objects.all()
        return HttpResponseRedirect(reverse('vendor_products'),{
        'categories':categories,
        'products':products        
    })


@login_required
def delete_product(request, pk):
    """ try:    
        product = Product.objects.filter(user=request.user).get(pk=pk)
        product.delete()
    except ObjectDoesNotExist:
        return render(request, 'userprofile/vendor_products.html', {'error': 'Product does not exist','categories':categories}) """
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()
    products=request.user.products.exclude(status=Product.DELETED)
    categories=Category.objects.all()
    return HttpResponseRedirect(reverse('vendor_products'),{
        'categories':categories,
        'products':products        
    })
    
@login_required
def vendor_products(request):

    categories=Category.objects.all()
    products=request.user.products.exclude(status=Product.DELETED)
    return render(request, 'userprofile/vendor_products.html',{
        'categories':categories,
        'products':products
    })

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    userprofile = Userprofile.objects.filter(user=user)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/vendor_detail.html', {
        'user' : user,
        'products' : products,
        'userprofile':userprofile
    })
@login_required
def vendor_profile(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/vendor_profile.html', {
        'user' : user,
        'products' : products
    })
@login_required
def vendor_account(request):
    return render(request, 'userprofile/vendor_account.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('frontpage'))
        else:
            return render(request, "userprofile/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "userprofile/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('frontpage'))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "userprofile/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
            Userprofile.objects.create(
                user=user,
            )
        except IntegrityError as e:
            print(e)
            return render(request, "userprofile/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('frontpage'))
    else:
        return render(request, "userprofile/register.html")
