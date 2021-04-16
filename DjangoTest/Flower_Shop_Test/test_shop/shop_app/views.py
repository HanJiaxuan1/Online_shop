from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

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
    # login_user = request.user
    # cart_list = Cart.objects.filter(user=login_user)

    # # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = CartForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         p_number = form.cleaned_data['number']
    #
    #         has_cart_item = False
    #         for old_cart_item in cart_list:
    #             if old_cart_item.product == selected_p:
    #                 has_cart_item = old_cart_item
    #
    #         if not has_cart_item:
    #             new_cart_item = Cart(product=selected_p, user=login_user, number=p_number)
    #             # save changes
    #             new_cart_item.save()
    #         else:
    #             has_cart_item.number += p_number
    #             has_cart_item.save()
    #         # redirect to a new URL:
    #         return cart(request)
    #
    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = CartForm()

    return render(request, 'product.html', {'product': selected_p})


@csrf_exempt
def add_to_cart(request):
    data = request.POST
    p_id = request.POST.get("p_id")
    p_num = request.POST.get("p_num")
    login_user = request.user
    selected_p = Product.objects.get(product_id=p_id)
    cart_list = Cart.objects.filter(user=login_user)

    # new_cart_item = Cart(product=selected_p, user=login_user, number=p_num)
    # new_cart_item.save()

    has_cart_item = False
    for old_cart_item in cart_list:
        if old_cart_item.product.product_id == p_id:
            has_cart_item = old_cart_item

    if not has_cart_item:
        new_cart_item = Cart(product=selected_p, user=login_user, number=p_num)
        # save changes
        new_cart_item.save()
    else:
        has_cart_item.number += p_num
        has_cart_item.save()

    response = JsonResponse({"p_id": p_id, "p_num": p_num})
    return response






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
    return render(request, 'about_us.html', {'user': request.user})


@csrf_exempt
def delete(request):
    data = request.POST
    getid = request.POST.get("getId")
    deleteObject = Cart.objects.get(cart_id=getid)
    deleteObject.delete()
    response = JsonResponse({"getId": getid})
    return response


@csrf_exempt
def changenumber(request):
    data = request.POST
    changenumber = request.POST.get("changenumber")
    getid = request.POST.get("getId")
    # changeObject = Cart.objects.get(cart_id = getid)
    # changeObject.update(number=changenumber)
    changeObject = Cart.objects.get(cart_id=getid)
    changeObject.number = changenumber
    changeObject.save()
    print(changeObject)
    # Cart.objects.filter(cart_id=getid).update(number=changenumber)
    response = JsonResponse({"getId": getid})
    return response


def addToOrder(request):
    user = request.user
    choices = request.POST.getlist('choice')
    if not choices:
        # Redisplay the cart form.
        return render(request, 'cart.html', {
            'user': user,
            'cart_list': Cart.objects.filter(user=user),
        })
    else:
        selected_choice = []
        for choice in choices:
            selected_choice.append(Cart.objects.filter(user=user).get(pk=choice))
        s = ''
        for item in selected_choice:
            s = s + str(item.product_id) + ':' + str(item.number) + ';'
            item.delete()
        selected_order = Order(user=request.user, order_list=s)
        selected_order.save()
        return HttpResponseRedirect(reverse('shop_app:order', args=(selected_order.order_id,)))


class ProductInfo:
    product_obj = 'obj'
    product_num = 'num'

    def __init__(self, obj, num):
        self.product_num = num
        self.product_obj = obj


def order(request, order_id):
    selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
    info = selected_order.order_list
    product_details = info.split(';')
    p_list = []
    for detail in product_details:
        if detail != '':
            product_obj = Product.objects.get(pk=int(detail.split(':')[0]))
            product_num = detail.split(':')[1]
            p_list.append(ProductInfo(product_obj, product_num))
    return render(request, 'order.html', {'product_list': p_list, 'order_id': order_id})


def payOrder(request, order_id):
    selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
    selected_order.status = 'paid'
    selected_order.save()
    return index(request)
