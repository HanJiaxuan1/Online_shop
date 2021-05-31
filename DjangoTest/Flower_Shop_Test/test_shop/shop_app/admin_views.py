import datetime

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
from .views import QuestionInfo, time_delta


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
    return HttpResponseRedirect(reverse('shop_app_question:question_detail', args=(question.question_id,)))

def statistics(request):
    return render(request, 'commercial.html')