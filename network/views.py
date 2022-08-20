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

@csrf_exempt
@login_required
def edit_post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Update the requested post
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            print(data["content"])
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    # Request method must be PUT
    else:
        return JsonResponse({
            "error": "PUT request required"
        }, status=400)

