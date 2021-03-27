from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import Product



def index(request):
    price_p_list = Product.objects.order_by('price')
    context = {
        'price_p_list': price_p_list,
    }
    return render(request, 'index.html', context)

def product(request, product_id):
    selected_p = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': selected_p})


def profile(request):
    # global logedin_user
    # if request.user.is_authenticated:
    #     logedin_user = get_object_or_404(Profile, request.user.username)
    return render(request, 'profile.html', {'user': request.user})

def cart(request):
    # global logedin_user
    # if request.user.is_authenticated:
    #     logedin_user = get_object_or_404(Profile, request.user.username)
    return render(request, 'cart.html', {'user': request.user})
