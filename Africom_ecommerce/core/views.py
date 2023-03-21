from django.shortcuts import render

from store.models import Product

def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)

    return render(request, 'core/frontpage.html', {
        'products': products
    })

def about(request):
    return render(request, 'core/about.html')