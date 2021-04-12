from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import Product, Cart, Order
from .forms import CartForm



def index(request):
    price_p_list = Product.objects.order_by('price')
    context = {
        'price_p_list': price_p_list,
    }
    return render(request, 'index.html', context)

def product(request, product_id):

    selected_p = get_object_or_404(Product, pk=product_id)
    login_user = request.user
    cart_list = Cart.objects.filter(user=login_user)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CartForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            p_number = form.cleaned_data['number']

            has_cart_item = False
            for old_cart_item in cart_list:
                if old_cart_item.product == selected_p:
                    has_cart_item = old_cart_item

            if not has_cart_item:
                new_cart_item = Cart(product=selected_p, user=login_user, number=p_number)
                # save changes
                new_cart_item.save()
            else:
                has_cart_item.number += p_number
                has_cart_item.save()


            # redirect to a new URL:
            return cart(request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CartForm()

    return render(request, 'product.html', {'form': form, 'product': selected_p})


def profile(request):
    # global logedin_user
    # if request.user.is_authenticated:
    #     logedin_user = get_object_or_404(Profile, request.user.username)
    return render(request, 'profile.html', {'user': request.user})

def cart(request):
    # global logedin_user
    # if request.user.is_authenticated:
    #     logedin_user = get_object_or_404(Profile, request.user.username)
    login_user = request.user
    cart_list = Cart.objects.filter(user=login_user)
    return render(request, 'cart.html', {'user': login_user, 'cart_list': cart_list})

def about_us(request):

    login_user = request.user

    return render(request, 'about_us.html',{'user': request.user})
