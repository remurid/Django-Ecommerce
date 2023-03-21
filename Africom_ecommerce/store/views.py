from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Order, Product, Category, Orderitem
from django.db.models import Q
from .cart import Cart
# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return HttpResponseRedirect(reverse('cart_view'))

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)
        return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')


def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart':cart
    })

def checkout(request):
    cart = Cart(request)
    if cart.get_total_cost == 0:
        return redirect('cart_view')
    
    if request.method == 'POST':
        total_price = 0
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        
        address = request.POST["address"]
        city = request.POST["city"]
        
        
        for item in cart:
            product = item['product']
            total_price += product.price * int(item['quantity'])
        order = Order(
            first_name=first_name,
            last_name =last_name,
            address =address,
            city=city,
            paid_amount=total_price,
            is_paid=False,
            
            
        )
        
        order.save()
        

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            item = Orderitem.objects.create(order=order, product=product, price=price, quantity=quantity)

        cart.clear()
        return redirect('frontpage')
    
    return render(request, 'store/checkout.html', {
        'cart':cart
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html', {
        'products':products,
        'query':query
    })  


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'store/category_detail.html', {
        'category' : category,
        'products' : products
    })

def product_detail(request, category_slug, slug):
    
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)

    return render(request, 'store/product_detail.html', {
        'product': product
    })