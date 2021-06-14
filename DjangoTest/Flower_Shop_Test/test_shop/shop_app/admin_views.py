import datetime
from django.utils.timezone import now, timedelta


from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, Order, Question, QuestionDetails, Favorite, Profile
from .forms import CartForm
from .views import QuestionInfo, time_delta, OrderInfo, ProductInfo


def question(request):
    question_all_list = Question.objects.order_by('-question_id')
    question_list = []
    for question in question_all_list:
        question_list.append(QuestionInfo(question.question_id, question.question_text, question.category,
                                          time_delta(question.date)))
    context = {
        'question_list': question_list,
    }
    return render(request, 'admin_question.html', context)


def question_detail(request, question_id):
    selected_q = get_object_or_404(Question, pk=question_id)
    detail_list = QuestionDetails.objects.filter(question=selected_q)

    return render(request, 'admin_question_detail.html', {'question': selected_q, 'detail_list': detail_list})


def admin_message(request, question_id):
    message_text = request.POST.get('message_text')
    question = Question.objects.get(question_id=question_id)
    new_message = QuestionDetails(question=question, answer_text=message_text,
                                  source='staff',
                                  date=datetime.datetime.now().strftime('%I:%M %p, %m.%d'))
    new_message.save()
    return HttpResponseRedirect(reverse('admin_question:question_detail', args=(question.question_id,)))


def statistics(request):
    # total_user number
    total_user = User.objects.filter().count()

    # total_order number and week_order number
    total_order = Order.objects.filter().count()
    start_date = now().date() + timedelta(days=-6)  # 一周前
    end_date = now().date() + timedelta(days=+1)
    print(start_date)
    week_order = Order.objects.filter(date__range=(start_date, end_date)).count()

    # total_bouquet number and total_profile
    selected_total_order = Order.objects.filter().all()
    total_bouquet = 0
    total_profile = 0
    rose = 0
    carnation = 0
    lily = 0
    diy = 0
    sunflower = 0
    tulips = 0
    for item in selected_total_order:
        info = item.order_list
        total_product_details = info.split(';')
        for product in total_product_details:
            product = product.split(':')
            if product[0] != '':
                total_bouquet += int(product[1])
                product_id = product[0]
                choose_product = Product.objects.get(product_id=product_id)
                total_profile = total_profile + choose_product.price
                if choose_product.type == "Rose":
                    rose += int(product[1])
                elif choose_product.type == "Carnation":
                    carnation += int(product[1])
                elif choose_product.type == "Lily":
                    lily += int(product[1])
                elif choose_product.type == "Sunflower":
                    sunflower += int(product[1])
                elif choose_product.type == "Tulips":
                    tulips += int(product[1])
                else:
                    diy += int(product[1])

    # week_bouquet number and week_profile
    selected_week_order = Order.objects.filter(date__range=(start_date, end_date)).all()
    print (selected_week_order)
    week_bouquet = 0
    week_profile = 0
    for item in selected_week_order:
        print (item)
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                week_bouquet += int(product[1])
                choose_product = product[0]
                choose_product = Product.objects.get(product_id=choose_product)
                week_profile = week_profile + choose_product.price


    # week info
    week1 = str(end_date + timedelta(days=-1)) + " to " + str(start_date)
    week2 = str(end_date + timedelta(days=-8)) + " to " + str(start_date + timedelta(days=-7))
    week3 = str(end_date + timedelta(days=-15)) + " to " + str(start_date + timedelta(days=-14))
    week4 = str(end_date + timedelta(days=-22)) + " to " + str(start_date + timedelta(days=-21))
    week5 = str(end_date + timedelta(days=-29)) + " to " + str(start_date + timedelta(days=-28))
    week6 = str(end_date + timedelta(days=-36)) + " to " + str(start_date + timedelta(days=-35))

    selected_order = Order.objects.filter(date__range=(start_date + timedelta(days=-7), end_date + timedelta(days=-7))).all()
    number2 = 0
    for item in selected_order:
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                number2 += int(product[1])

    selected_order = Order.objects.filter(date__range=(start_date + timedelta(days=-14), end_date + timedelta(days=-14))).all()
    number3 = 0
    for item in selected_order:
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                number3 += int(product[1])

    selected_order = Order.objects.filter(date__range=(start_date + timedelta(days=-21), end_date + timedelta(days=-21))).all()
    number4 = 0
    for item in selected_order:
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                number4 += int(product[1])

    selected_order = Order.objects.filter(date__range=(start_date + timedelta(days=-28), end_date + timedelta(days=-28))).all()
    number5 = 0
    for item in selected_order:
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                number5 += int(product[1])

    selected_order = Order.objects.filter(date__range=(start_date + timedelta(days=-35), end_date + timedelta(days=-35))).all()
    number6 = 0
    for item in selected_order:
        info = item.order_list
        week_product_details = info.split(';')
        for product in week_product_details:
            product = product.split(':')
            if product[0] != '':
                number6 += int(product[1])

    return render(request, 'commercial.html', {'total_order': total_order, 'week_order': week_order,
                                               'total_profile': total_profile, 'week_profile': week_profile,
                                               'total_bouquet': total_bouquet, 'week_bouquet': week_bouquet,
                                               'total_user': total_user, 'rose': rose, 'carnation': carnation,
                                               'lily': lily, 'diy': diy, 'sunflower':sunflower,
                                               'tulips': tulips, 'week1': week1, 'week2': week2,
                                               'week3': week3,'week4': week4,'week5': week5,'week6': week6,
                                               'number1': week_bouquet, 'number2': number2,'number3': number3,
                                               'number4': number4,'number5': number5,'number6': number6})


def order(request):
    # order_all_list = Order.objects.order_by('order_id')
    # order_list = []
    # for order in order_all_list:
    #     order_list.append(OrderInfo(order.order_id, order.
    #                                       time_delta(question.date)))
    # context = {
    #     'question_list': question_list,
    # }
    # return render(request, 'admin_question.html', context)

    #     logedin_user = get_object_or_404(Profile, request.user.username)


    order_list = Order.objects.order_by('-order_id')

    o_list = []
    for a_order in order_list:
        order_id = a_order.order_id
        user_id = a_order.user.id
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

        o_list.append(OrderInfo(p_list, order_id, user_id, total_price, order_date, a_order.status, pic1, pic2, order_receiver,
                                order_phone, order_address))
    return render(request, 'admin_history_order.html', {'order_list': o_list})