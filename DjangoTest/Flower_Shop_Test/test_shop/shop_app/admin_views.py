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


def question(request):
    question_list = Question.objects.order_by('question_id')
    context = {
        'question_list': question_list,
    }
    return render(request, 'admin_question.html', context)


def question_detail(request, question_id):
    selected_q = get_object_or_404(Question, pk=question_id)
    detail_list = QuestionDetails.objects.filter(question=selected_q)

    return render(request, 'admin_question_detail.html', {'detail_list': detail_list})
