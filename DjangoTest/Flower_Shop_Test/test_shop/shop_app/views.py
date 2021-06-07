import datetime
import os
from random import random

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
import random
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, Order, Question, QuestionDetails, Favorite, Profile, Address, DefaultAddress, \
    EpidemicMode, ProductComment
from .forms import CartForm, AddPhotoForm
import base64
import shutil


def index(request):
    price_p_list = Product.objects.order_by('price')
    context = {
        'price_p_list': price_p_list,
    }
    return render(request, 'index.html', context)


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


class Comment:
    text = ''
    username = ''
    user_portrait = ''
    time_d = ''

    def __init__(self, t, n, p, d):
        self.text = t
        self.username = n
        self.user_portrait = p
        self.time_d = d


def product(request, product_id):
    selected_p = get_object_or_404(Product, pk=product_id)
    s_comment = ProductComment.objects.filter(product=selected_p).order_by('-date')
    comments = []
    # print(Profile.objects.get(userinfo_id=s_comment[0].user.id).photo)
    for comment in s_comment:
        comments.append(Comment(comment.text, comment.user.username,
                                Profile.objects.get(userinfo_id=comment.user.id).photo,
                                time_delta(comment.date)))
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

    return render(request, 'product.html', {'product': selected_p, 'comments': comments})


def add_comment(request, product_id):
    comment_text = request.POST.get('comment_text')
    s_product = Product.objects.get(pk=product_id)
    user = request.user
    new_comment = ProductComment(text=comment_text, product=s_product, user=user)
    new_comment.save()
    return HttpResponseRedirect(reverse('shop_app:detail', args=(product_id,)))


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

                if old_cart_id == p_id:
                    has_cart_item = old_cart_item


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

@csrf_exempt
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
        # return render(request, 'profile.html', {'user': request.user, 'profile': profile}, )
        if request.method == "POST":
            af = AddPhotoForm(request.FILES)
            pic = request.FILES.get('photo')  # 'pic'对应前端表单的name属性值。
            print(pic)
            filename = str(uid) + "_" + pic.name
            print(filename)
            save_path = '%s/user/%s'%(settings.MEDIA_ROOT,filename) # pic.name 上传文件的源文件名

            # 判断表单值是否和法
            if af.is_valid():
                with open(save_path, 'wb') as f:
                    # 获取上传文件的内容并写到创建的文件中
                    for content in pic.chunks():  # pic.chunks() 上传文件的内容。
                        f.write(content)
                print("yes")
                # headimg = af.cleaned_data['photo']
                changeObject = Profile.objects.filter(userinfo_id=uid)
                photo = changeObject.update(photo=filename)
                # return render(request, 'profile.html', context={"photo":photo})
                # return render(request, 'profile.html', {'user': request.user, 'profile': profile,
                #                                         'photo':photo, 'af':af}, )
                return redirect('/profile/', {'user': request.user, 'profile': profile,
                                                        'photo':photo, 'af':af}, )
            else:
                print("no")
                # 打印错误信息
                print(af.errors.get_json_data())
                message = af.errors.get_json_data()['photo'][0]
                message = message['message']
                return render(request, 'profile.html', {'user': request.user, 'profile': profile,
                                                        'af':af, 'msg':message}, )

        else:
            af = AddPhotoForm()
            return render(request, 'profile.html', {'user': request.user, 'profile': profile, 'af':af}, )
            # return render(request, 'profile.html', context={"af":af})
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
        changeUserObject.update(username=username, first_name=firstname, last_name=lastname, email=email)
    else:
        changeObject.update(userinfo_id=getid, date_of_birth=birthday, phone=phone, region=region)
        changeUserObject.update(username=username, first_name=firstname, last_name=lastname, email=email)
    response = JsonResponse({"getId": getid})
    return response


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


class ProductInfo:
    product_obj = 'obj'
    product_num = 'num'

    def __init__(self, obj, num):
        self.product_num = num
        self.product_obj = obj


class OrderInfo:
    products = []
    order_id = '0'
    total_price = '1'
    order_date = 'today'
    status = 'null'
    pic1 = ''
    pic2 = ''

    def __init__(self, product_info, order_id, price, date, status, pic1, pic2, order_receiver, order_phone, order_address):
        self.products = product_info
        self.order_id = order_id
        self.total_price = price
        self.order_date = date
        self.status = status
        self.pic1 = pic1
        self.pic2 = pic2
        self.order_receiver = order_receiver
        self.order_phone = order_phone
        self.order_address = order_address

    def __str__(self):
        return '%s  %s  %s' % (self.total_price, self.order_date, self.status)


def history_order(request):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user
        order_list = Order.objects.filter(user=login_user).order_by('-order_id')

        o_list = []
        for a_order in order_list:
            order_id = a_order.order_id
            order_receiver = a_order.receiver
            order_phone = a_order.phone
            order_address = a_order.address
            product_details = a_order.order_list.split(';')
            total_price = 0
            order_date = a_order.date.strftime('%y/%m/%d')
            p_list = []
            i = 1
            pic1 = ''
            pic2 = ''
            for detail in product_details:
                if detail != '':
                    product_obj = Product.objects.get(pk=int(detail.split(':')[0]))
                    product_num = detail.split(':')[1]
                    total_price = total_price + int(product_obj.price) * int(product_num)
                    if i == 1:
                        pic1 = product_obj.product_image
                    if i == 2:
                        pic2 = product_obj.product_image
                    p_list.append(ProductInfo(product_obj, product_num))
                i = i + 1

            o_list.append(OrderInfo(p_list, order_id, total_price, order_date, a_order.status, pic1, pic2,order_receiver,order_phone,order_address))
        return render(request, 'history_order.html', {'order_list': o_list})
    else:
        return HttpResponseRedirect(reverse('account:login'))


def address(request):
    if request.user.is_authenticated:
        login_user = request.user.id
        address_list = Address.objects.filter(user_id=login_user)
        defaultAddress = DefaultAddress.objects.filter(user_id=login_user)
        return render(request, 'address.html', {'user': login_user,
                                                'address_list': address_list,
                                                'default_address': defaultAddress}, )
    else:
        return HttpResponseRedirect(reverse('account:login'))


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
                # print(address_list)
                # print(old_address)
                # print(old_category)
                # print(address)
                # print(category)
                if old_category == category and old_address == address:
                    print("存在")
                    response = JsonResponse({"msg": "This Address already existed!"})
                    return response

            print("不存在")
            new_address = Address(user_id=login_user.id, address=address, category=category)
            new_address.save()
            response = JsonResponse({"msg": "New Address Successfully Added to Your Address"})
            return response
    else:
        response = JsonResponse({"msg": "Please login first"})
        return response


@csrf_exempt
def edit_address(request):
    if request.user.is_authenticated:
        getid = request.POST.get("getId")
        login_user = request.user
        category = str(request.POST.get("category"))
        address = str(request.POST.get("address"))
        address_list = Address.objects.filter(user=login_user)
        for old_address_item in address_list:
            old_address = str(old_address_item.address)
            old_category = str(old_address_item.category)
            if old_category == category and old_address == address:
                print("存在")
                response = JsonResponse({"msg": "This Address already existed!"})
                return response
        print("不存在")
        editobject = Address.objects.filter(address_id=getid)
        # print(editobject)
        editobject.update(address=address, category=category)
        response = JsonResponse({"msg": "The address was updated successfully!"})
        return response
    else:
        response = JsonResponse({"msg": "Please login first"})
        return response


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
    pid = changeObject.product_id
    item = Product.objects.get(product_id=pid)
    # Cart.objects.filter(cart_id=getid).update(number=changenumber)
    response = JsonResponse({"item": item.product_name})
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


def order(request, order_id):
    user = request.user
    selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
    order_status = selected_order.status
    info = selected_order.order_list
    product_details = info.split(';')
    p_list = []
    defaultAddress = DefaultAddress.objects.filter(user_id=request.user.id)
    for detail in product_details:
        if detail != '':
            product_obj = Product.objects.get(pk=int(detail.split(':')[0]))
            product_num = detail.split(':')[1]
            int_num = int(product_num)

            product_obj.inventory -= int_num
            product_obj.save()

            p_list.append(ProductInfo(product_obj, product_num))
    # print(p_list)

    return render(request, 'order.html', {'product_list': p_list,
                                          'order_id': order_id,
                                          'order_status': order_status,
                                          'user': request.user,
                                          'default_address': defaultAddress})


@csrf_exempt
def add_cart_again(request, order_id):
    # order_id = request.POST.get('order_id')
    user = request.user.id
    selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
    product_list = selected_order.order_list
    product_details = product_list.split(';')
    for detail in product_details:
        if detail != '':
            product_obj = detail.split(':')[0]
            product_num = detail.split(':')[1]
            int_num = int(product_num)
            changeObject = Cart.objects.create(user_id=user, product_id=product_obj,
                                               number=int_num)
            selected_order.delete()
            print(changeObject)
    response = JsonResponse({"getId": user})
    return response


@csrf_exempt
def cancel_order(request, order_id):
    # order_id = request.POST.get('order_id')
    user = request.user.id
    selected_order = Order.objects.filter(user=request.user).get(pk=order_id)
    selected_order.delete()
    response = JsonResponse({"getId": user})
    return response


def orderNow(request, product_id):
    if request.user.is_authenticated:
        #     logedin_user = get_object_or_404(Profile, request.user.username)
        login_user = request.user

        s = str(product_id) + ':' + '1' + ';'
        selected_order = Order(user=request.user, order_list=s)
        selected_order.save()
        return HttpResponseRedirect(reverse('shop_app:order', args=(selected_order.order_id,)))

    else:
        return HttpResponseRedirect(reverse('account:login'))



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
    result = random.randint(4, 15)
    result_p = get_object_or_404(Product, pk=result)
    login_user = request.user
    return render(request, 'result.html', {'user': request.user, 'product': result_p})


def DIY(request):
    login_user = request.user
    return render(request, 'DIY.html', {'user': request.user})


@csrf_exempt
def checkMode(request):
    mode = EpidemicMode.objects.get(pk=1).mode
    print(str(mode))
    return JsonResponse({"msg": str(mode)})


@csrf_exempt
def savePic(request):
    data = request.POST.get('dataURL')
    pic_name = str(request.user.id)+'_DIY.png'
    imagedata = base64.b64decode(data)
    with open('./media/media/static/product/'+pic_name, 'wb') as f:
        f.write(imagedata)
    return JsonResponse({"msg": 'good'})

@csrf_exempt
def savePicOrder(request):

    data = str(request.POST.get('dataSRC'))
    order_id = request.POST.get('order_id')
    pic_name = str(request.user.id)+'_'+str(order_id)+'_DIY.png'
    data = data.strip('/')

    old_path = data
    new_path = 'media/user/diy/' + pic_name
    # new_path = 'media/media/static/product/1_4_DIY.png'
    shutil.copy(old_path, new_path)
    # os.renames(old_path, new_path)

    # imagedata = base64.b64decode(data)
    # with open('./media/user/diy/'+pic_name, 'wb') as f:
    #     f.write(imagedata)
    return JsonResponse({"msg": 'good'})
