import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator

from .models import *

def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def compose(request):

    # Get post body data
    data = json.loads(request.body)
    content = data.get("content")

    # If change post
    if (data.get("change")):
        post = Post.objects.get(pk=int(data.get("post_id")))
        post.content = data.get("content")
        post.save()

        return JsonResponse({"messege": "Post changed successfully."}, status=201)

    # Return error if body empty
    if content == None or content == "":
        return JsonResponse({
            "error": "Post body is empty."
        }, status=400)

    # Create one post for the user
    post = Post(
        person=request.user,
        content=content
    )
    post.save()
    print("Arrived")

    return JsonResponse({"messege": "Post published successfully."}, status=201)

@csrf_exempt
def profile(request, poster_id):

    # Get data
    poster = User.objects.get(id=poster_id)
    followers = Follower.objects.filter(influencer_id=poster_id).count()

    if Follower.objects.filter(person=poster).count() != 0:
        following_users = Follower.objects.filter(person=poster)
        followings_num = following_users.count()
        following_users = [following_user.serialize() for following_user in following_users]
    else:
        following_users = "NONE"
        followings_num = 0

    try:
        user_id = request.user.id
        follow = check_follow(request.user, poster_id)
    except:
        # If not signed in
        user_id = "NONE"
        follow = "NONE"

    return JsonResponse({
        "user_id": user_id,
        "username": poster.username,
        "followers": followers,
        "follow": follow,
        "followings_num": followings_num,
        "followings": following_users
    }, safe=False)

@login_required
def follow(request, poster_id):
    follow = check_follow(request.user, poster_id)
    if follow == "Follow":
        follower = Follower(
            influencer_id=poster_id,
            influencer_name=User.objects.get(pk=poster_id).username,
            person=request.user
        )
        follower.save()
    else:
        follower = Follower.objects.filter(person=request.user).get(influencer_id=poster_id)
        follower.delete()

    return HttpResponse(status=204)

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    like = check_like(request.user.id, post_id)
    if like == "Like":
        like_obj = Like(
            person_id=request.user.id,
            post_id=post_id
        )
        like_obj.save()

        # Update likes attribute of model post
        post.likes += 1
        post.save()
    else:
        like_obj = Like.objects.filter(person_id=request.user.id).get(post_id=post_id)
        like_obj.delete()
        post.likes -= 1
        post.save()

    return JsonResponse({"value": like, "post_like": post.likes}, safe=False)

def check_follow(user, poster_id):
    if user.id != poster_id:
        # If user not follow poster
        if Follower.objects.filter(person=user).filter(influencer_id=poster_id).count() == 0:
            follow = "Follow"
        else:
            follow = "Unfollow"
    else:
        follow = "None"

    return follow

def check_like(user_id, post_id):
    # If likes, return unlike string
    if Like.objects.filter(person_id=user_id).filter(post_id=post_id).count() > 0:
        return "Unlike"
    else:
        return "Like"

@csrf_exempt
def postbox(request, user_id=None):
    ## user_id: the id of request.user

    # If all-posts button is clicked
    if user_id == None:
        # Get the posts
        posts = Post.objects

    elif json.loads(request.body).get("profile"):
    # If for profile
        poster = User.objects.get(pk=user_id)
        posts = Post.objects.filter(person=poster)
    # If following button is clicked
    # Error messege changed from "you" to "this poster"
    else:
        influencer_ids = User.objects.get(id=user_id).following.values_list('influencer_id', flat=True)

        try:
            posts = User.objects.get(pk__in=influencer_ids).posts

        except:
            return JsonResponse({"error": "You have not followed anyone yet."}, status=400)

     # Use reverse chronological order
    posts = posts.order_by("-time").all()

    # Implement pagination
    # Show ten posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # If previous page
    if page_obj.has_previous():
        previous = page_obj.previous_page_number()
    else:
        previous = 0
    # If next page
    if page_obj.has_next():
        nex = page_obj.next_page_number()
    else:
        nex = 0

    # Implement like list with first pair as length of posts
    likes = {"length":len(page_obj.object_list)}
    for post, i in zip(page_obj, list(range(10))):
        likes[i] = check_like(request.user.id, post.pk)

    return JsonResponse([[post.serialize() for post in page_obj], {
        "has_previous": page_obj.has_previous(),
        "previous_page_number": previous,
        "num_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "next_page_number": nex,
        "user_id": request.user.id
    }, likes], safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
