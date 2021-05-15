import datetime
from random import random

from django.shortcuts import render, get_object_or_404

# Create your views here.
import random
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, Order, Question, QuestionDetails, Favorite, Profile, Address, DefaultAddress
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
    if request.user.is_authenticated:
        data = request.POST
        p_id = str(request.POST.get("p_id"))
        p_num = int(request.POST.get("p_num"))
        login_user = request.user
        selected_p = Product.objects.get(product_id=p_id)
        cart_list = Cart.objects.filter(user=login_user)

        # new_cart_item = Cart(product=selected_p, user=login_user, number=p_num)
        # new_cart_item.save()

        if selected_p.inventory >= p_num:
            # selected_p.inventory -= p_num
            # selected_p.save()

            has_cart_item = False
            for old_cart_item in cart_list:
                old_cart_id = str(old_cart_item.product.product_id)
                print(old_cart_id)
                if old_cart_id == p_id:
                    has_cart_item = old_cart_item
                    print("has_cart_item: ")
                    print(has_cart_item)

            if not has_cart_item:
                new_cart_item = Cart(product=selected_p, user=login_user, number=p_num)
                # save changes
                new_cart_item.save()
            else:
                has_cart_item.number += p_num
                has_cart_item.save()

            response = JsonResponse({"msg": "Product Successfully Added to Cart"})
            return response
        else:

            response = JsonResponse({"msg": "Request is larger than inventory"})
            return response
    else:
        response = JsonResponse({"msg": "Please login first"})
        return response


@csrf_exempt
def add_address(request):
    if request.user.is_authenticated:
        data = request.POST
        login_user = request.user
        category = str(request.POST.get("category"))
        address = str(request.POST.get("address"))
        address_list = Address.objects.filter(user=login_user)
        if not address_list:
            new_address = Address(user_id=login_user.id, address=address, category=category)
            new_address.save()
            response = JsonResponse({"msg": "New Address Successfully Added to Your Address"})
            return response
        else:
            for old_address_item in address_list:
                old_address = str(old_address_item.address)
                old_category = str(old_address_item.category)
                print(old_address)
                print(old_category)
                if old_category == category and old_address == address:
                    response = JsonResponse({"msg": "This Address already existed!"})
                else:
                    new_address = Address(user_id=login_user.id, address=address, category=category)
                    new_address.save()
                    response = JsonResponse({"msg": "New Address Successfully Added to Your Address"})
                return response
    else:
        response = JsonResponse({"msg": "Please login first"})
        return response


@csrf_exempt
def add_to_favorite(request):
    if request.user.is_authenticated:
        data = request.POST
        p_id = str(request.POST.get("p_id"))
        login_user = request.user
        selected_p = Product.objects.get(product_id=p_id)
        favorite_list = Favorite.objects.filter(user=login_user)
        has_favorite_item = False
        for old_favorite_item in favorite_list:
            old_favorite_id = str(old_favorite_item.product.product_id)
            print(old_favorite_id)
            if old_favorite_id == p_id:
                has_favorite_item = old_favorite_item
        if not has_favorite_item:
            new_favorite_item = Favorite(product=selected_p, user=login_user)
            # save changes
            new_favorite_item.save()

        response = JsonResponse({"msg": "Product Successfully Added to Your Favorite"})
        return response

    else:
        response = JsonResponse({"msg": "Please login first"})
        return response


@csrf_exempt
def add_order(request):
    if request.user.is_authenticated:
        data = request.POST
        order_id = str(request.POST.get("o_id"))
        receiver = str(request.POST.get("receiver"))
        phone = int(request.POST.get("phone"))
        address = str(request.POST.get("address"))

        selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
        selected_order.status = 'paid'
        selected_order.receiver = receiver
        selected_order.phone = phone
        selected_order.address = address
        selected_order.save()
        response = JsonResponse({"msg": "The order has been set, thank you for purchase!"})
        return response


#
# def payOrder(request, order_id):
#     selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
#     selected_order.status = 'paid'
#     selected_order.save()
#     return index(request)


def profile(request):
    # global logedin_user
    # if request.user.is_authenticated:
    #     logedin_user = get_object_or_404(Profile, request.user.username)
    if request.user.is_authenticated:
        uid = request.user.id
        profile = Profile.objects.filter(userinfo_id=uid).all()
        if not profile:
            profile = Profile.objects.create(userinfo_id=uid)
        else:
            profile = profile[0]
        return render(request, 'profile.html', {'user': request.user, 'profile': profile},)
    else:
        return HttpResponseRedirect(reverse('account:login'))


def cart(request):
    # global logedin_user
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        cart_list = Cart.objects.filter(user=login_user)
        return render(request, 'cart.html', {'user': login_user,
                                             'cart_list': cart_list,
                                             'error': ""}, )
    else:
        return HttpResponseRedirect(reverse('account:login'))


def about_us(request):
    login_user = request.user
    return render(request, 'about_us.html', {'user': request.user})


class QuestionInfo:
    question_id = "id"
    question_text = 'text'
    question_category = 'cate'
    time_differ = 'delta'

    def __init__(self, ide, text, cate, delta):
        self.question_id = ide
        self.question_text = text
        self.question_category = cate
        self.time_differ = delta


def time_delta(date_time):
    day_delta = (datetime.datetime.now() - date_time).days
    if day_delta > 0:
        return str(day_delta) + 'd ago'
    delta = (datetime.datetime.now() - date_time).seconds
    day = delta // 84600
    hour = delta // 3600
    minute = delta // 60
    if 0 <= delta < 60:
        return 'just now'
    elif 60 <= delta < 3600:
        return str(minute) + 'm ago'
    elif 3600 <= delta < 86400:
        return str(hour) + 'h ago'
    else:
        return str(day) + 'd ago'


def service(request):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        question_all_list = Question.objects.filter(user=login_user).order_by('-question_id')
        question_list = []
        for question in question_all_list:
            question_list.append(QuestionInfo(question.question_id, question.question_text, question.category,
                                              time_delta(question.date)))
        return render(request, 'service.html', {'question_list': question_list})
    else:
        return HttpResponseRedirect(reverse('account:login'))


def communication(request, question_id):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        question = Question.objects.get(user=login_user, question_id=question_id)
        question_detail = QuestionDetails.objects.filter(question=question)
        return render(request, 'communication.html', {'question': question, 'question_detail': question_detail})
    else:
        return HttpResponseRedirect(reverse('account:login'))


def history_order(request):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        cart_list = Cart.objects.filter(user=login_user)
        return render(request, 'history_order.html')
    else:
        return HttpResponseRedirect(reverse('account:login'))


def address(request):
    if request.user.is_authenticated:
        login_user = request.user.id
        address_list = Address.objects.filter(user_id=login_user)
        defaultAddress = DefaultAddress.objects.filter(user_id=login_user)
        return render(request, 'address.html', {'user': login_user,
                                             'address_list': address_list,
                                             'default_address':defaultAddress},)
    else:
        return HttpResponseRedirect(reverse('account:login'))


@csrf_exempt
def delete_address(request):
    data = request.POST
    getid = request.POST.get("getId")
    deleteObject = Address.objects.get(address_id=getid)
    print(deleteObject)
    deleteObject.delete()
    response = JsonResponse({"msg": "You have successfully deleted an address"})
    return response


@csrf_exempt
def default_address(request):
    getuserid = request.POST.get("getUserId")
    getaddressid = request.POST.get("getAddressId")
    defaultAddress = DefaultAddress.objects.filter(user_id=getuserid)
    if not defaultAddress:
        DefaultAddress.objects.create(user_id=getuserid, default_address_id=getaddressid)
    else:
        defaultAddress.update(user_id=getuserid, default_address_id=getaddressid)
    response = JsonResponse({"msg": "You have successfully update your default address"})
    return response


def favorites(request):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        favorite_list = Favorite.objects.filter(user=login_user)
        return render(request, 'favorites.html', {'user': login_user,
                                             'favorite_list': favorite_list}, )
    else:
        return HttpResponseRedirect(reverse('account:login'))


@csrf_exempt
def change_profile(request):
    data = request.POST
    getid = request.POST.get("getId")
    username = request.POST.get("username")
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    birthday = request.POST.get("birthday")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    region = request.POST.get("region")
    changeObject = Profile.objects.filter(userinfo_id=getid)
    changeUserObject = User.objects.filter(id=getid)
    if not changeObject:
        Profile.objects.create(userinfo_id=getid, date_of_birth=birthday, phone=phone, region=region)
        changeUserObject.update(username=username, first_name=firstname, last_name=lastname, email=email )
    else:
        changeObject.update(userinfo_id=getid, date_of_birth=birthday, phone=phone, region=region)
        changeUserObject.update(username=username, first_name=firstname, last_name=lastname, email=email )
    response = JsonResponse({"getId": getid})
    return response


@csrf_exempt
def delete(request):
    data = request.POST
    getid = request.POST.get("getId")
    deleteObject = Cart.objects.get(cart_id=getid)
    deleteObject.delete()
    response = JsonResponse({"getId": getid})
    return response


@csrf_exempt
def delete_favorite(request):
    getid = request.POST.get("getId")
    deleteObject = Favorite.objects.get(favorite_id=getid)
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
            'error': "You have not choose any products yet"
        })
    else:
        selected_choice = []
        for choice in choices:
            selected_choice.append(Cart.objects.filter(user=user).get(pk=choice))
        s = ''

        for item in selected_choice:
            if int(item.product.inventory) < int(item.number):
                return render(request, 'cart.html', {
                    'user': user,
                    'cart_list': Cart.objects.filter(user=user),
                    'error': "Request is larger than inventory"
                })

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
            int_num = int(product_num)

            product_obj.inventory -= int_num
            product_obj.save()

            p_list.append(ProductInfo(product_obj, product_num))
    return render(request, 'order.html', {'product_list': p_list, 'order_id': order_id})


def orderNow(request, product_id):
    s = str(product_id) + ':' + '1' + ';'
    selected_order = Order(user=request.user, order_list=s)
    selected_order.save()
    return HttpResponseRedirect(reverse('shop_app:order', args=(selected_order.order_id,)))


def createQuestion(request):
    question_text = request.POST.get('question_text')
    category = request.POST.get('category')
    new_question = Question(user=request.user, question_text=question_text, category=category)
    new_question.save()
    return HttpResponseRedirect(reverse('shop_app:service'))


def userMessage(request, question_id):
    message_text = request.POST.get('message_text')
    question = Question.objects.get(user=request.user, question_id=question_id)
    new_message = QuestionDetails(question=question, answer_text=message_text,
                                  date=datetime.datetime.now().strftime('%I:%M %p, %m.%d'))
    new_message.save()
    return HttpResponseRedirect(reverse('shop_app:communication', args=(question.question_id,)))


def classifier(request):
    return render(request, 'classifier.html')


def prediction(request):
    login_user = request.user
    return render(request, 'prediction.html', {'user': request.user})


def result(request):
    result = random.randint(4,15)
    result_p=get_object_or_404(Product, pk=result)
    login_user = request.user
    return render(request, 'result.html', {'user': request.user, 'product': result_p} )


def DIY(request):
    login_user = request.user
    return render(request, 'DIY.html', {'user': request.user})