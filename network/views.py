import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    posts = Post.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
        "posts": posts
    })


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


def create_post(request):
    if request.method == "POST":
        content = request.POST['content']
        poster = request.user

        new_post = Post.objects.create(
            content = content,
            poster = poster
        )
        new_post.save()

    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(poster=user).order_by('-timestamp')

    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts
    }) 


@login_required
def following(request):
    follows = User.objects.get(username=request.user).follows.all()
    posts = Post.objects.filter(poster__in=follows).order_by('-timestamp')

    return render(request, "network/following.html", {
        "posts": posts
    })


#==================================================================================
@csrf_exempt
@login_required
def api_post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update the requested post
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        if data.get("user") is not None:
            user = User.objects.get(username=data["user"])
            if post.likers.all().contains(user):
                post.likers.remove(user)
            else:
                post.likers.add(user)
        post.save()
        return HttpResponse(status=204)
    
    # Request method must be PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


@csrf_exempt
@login_required
def api_profile(request, profile_id):
    # Query for requested user
    try:
        profile = User.objects.get(pk=profile_id)
    except:
        return JsonResponse({"error": "User not found."}, status=404)
    
    # Return user
    if request.method == "GET":
        return JsonResponse(profile.serialize())
#        return JsonResponse(user.serialize())

    # Update the requested user
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follower") is not None:
            follower = User.objects.get(username=data["follower"])
            if profile.followers.all().contains(follower):
                profile.followers.remove(follower)
                follower.follows.remove(profile)
            else:
                profile.followers.add(follower)
                follower.follows.add(profile)
        profile.save()
        return HttpResponse(status=204)
    
    # Request method must be PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)

    