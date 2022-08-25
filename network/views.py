import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    p = paginate_posts(request, posts)

    return render(request, "network/index.html", {
        "page_obj": p.get("page_obj"),
        "page_range": p.get("page_range"),
        "need_paginated": p.get("need_paginated")
    })


def paginate_posts(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')

    p = dict()
    p["page_obj"] = paginator.get_page(page_number)
    p["page_range"] = range(1, paginator.num_pages + 1)
    p["need_paginated"] = True if (paginator.num_pages > 1) else False

    return p


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(poster=user).order_by('-timestamp')

    p = paginate_posts(request, posts)

    return render(request, "network/profile.html", {
        "user": user,
        "page_obj": p.get("page_obj"),
        "page_range": p.get("page_range"),
        "need_paginated": p.get("need_paginated")
    }) 


@login_required
def following(request):
    follows = User.objects.get(username=request.user).follows.all()
    posts = Post.objects.filter(poster__in=follows).order_by('-timestamp')

    p = paginate_posts(request, posts)

    return render(request, "network/following.html", {
        "page_obj": p.get("page_obj"),
        "page_range": p.get("page_range"),
        "need_paginated": p.get("need_paginated")
    })


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

#==================================================================================
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

#==================================================================================
# API

@csrf_exempt
@login_required
def api_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None and request.user == post.poster:
            post.content = data["content"]
        if data.get("user") is not None:
            user = User.objects.get(username=data["user"])
            if post.likers.all().contains(user):
                post.likers.remove(user)
            else:
                post.likers.add(user)
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


@csrf_exempt
@login_required
def api_profile(request, profile_id):
    try:
        profile = User.objects.get(pk=profile_id)
    except:
        return JsonResponse({"error": "User not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(profile.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("current_user") is not None:
            current_user = User.objects.get(username=data["current_user"])
            switch_follow_state(current_user, profile)
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


def switch_follow_state(current_user, profile):
    if profile.followers.all().contains(current_user):
        profile.followers.remove(current_user)
        current_user.follows.remove(profile)
    else:
        profile.followers.add(current_user)
        current_user.follows.add(profile)
        
    current_user.save()
    profile.save()