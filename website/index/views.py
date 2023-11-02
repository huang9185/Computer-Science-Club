from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *

from datetime import date
import json

# Create your views here.
def index(request):
    return render(request, "index/index.html")

@login_required
def home(request):
    # From layout.html, home tab onclick
    if request.method == 'GET':
        return render(request, "index/home.html", {
            "message": "Hello, "+ request.user.username
        })

@csrf_exempt
@login_required
def vote(request, comment_id):
    # From question.html, vote button onclick, js fetch GET
    if request.method == 'GET':
        vote = Vote(
            user=request.user.id,
            comment=comment_id
        )
        vote.save()
        return JsonResponse(["Vote object created"], safe=False)

@csrf_exempt
@login_required
def comment(request, question_id):
    # From question.html, comment button onclick, js fetch
    data = json.loads(request.body)
    if request.method == 'POST':
        comment = Comment(
            question=question_id,
            content=data['content'],
            user=request.user.id
        )
        comment.save()

        return JsonResponse(["Comment created"], safe=False)

def question(request, question_id):
    # From faq.html, "details" button onclick
    if request.method == "GET":
        comments = Comment.objects.filter(question=question_id).order_by('-votes')
        comments_serialized = []
        
        for comment in comments:
            if Vote.objects.filter(comment=comment.id).filter(user=request.user.id).count():
                is_voted = True
            else:
                is_voted = False
            # Sync # of votes objects with actual votes field of comment
            comment.votes = Vote.objects.filter(comment=comment.id).count()
            comment.save()
            comments_serialized.append({
                "pk": comment.id,
                "time": comment.time,
                "content": comment.content,
                "user": User.objects.get(pk=comment.user).username,
                "votes": comment.votes,
                "is_voted": is_voted
            })

        try:
            is_member = User.objects.get(pk=request.user.id).is_member
        except:
            # User does not login
            is_member = False
        return render(request, "index/question.html", {
            "question": Question.objects.get(pk=question_id).serialize(),
            "comments": comments_serialized,
            "is_member": is_member
        })

@csrf_exempt
def faq(request):
    # From navigation bar, faq tab
    if request.method == "GET":
        questions = [question.serialize() for question in Question.objects.all().order_by('-time')]
        for question in questions:
            question['comments'] = Comment.objects.filter(question=question['pk']).count()
        return render(request, "index/faq.html", {
            "questions": questions
        })
    # From faq.html, submit button onclick, js fetch POST
    elif request.method == "POST":
        data = json.loads(request.body)
        question = Question(
            title=data['title'],
            content=data['content']
        )
        question.save()
        return JsonResponse(["Question created."], safe=False)

def dates(request):
    if request.method == "GET":
        return render(request, "index/dates.html", {
        'today': date.today().strftime("%B %d, %Y")
        })

def contact(request):
    if request.method == "GET":
        return render(request, "index/contact.html")

def register(request):
    # From login, link under form
    if request.method == "GET":
        return render(request, 'index/register.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        if User.objects.filter(username=username).count() or User.objects.filter(email=email).count():
            return render(request, 'index/register.html', {
                "error": "User already exists"
            })
        elif password == confirmation:
            user = User(
                username=username,
                email=email,
                password=password
            )
            user.save()
            login(request, user)
            return render(request, 'index/index.html')

        else:
            return render(request, 'index/register.html', {
                "error": "Form data is invalid"
            })

def login_view(request):
    # From index page, login link
    if request.method == "GET":
        return render(request, "index/login.html")

    # From login page, form submittion to create user
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(username=username).get(password=password)
            login(request, user)
            return render(request, 'index/index.html')
        except:
            return render(request, 'index/login.html', {
                "error": "User does not exist"
            })

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index/index.html')