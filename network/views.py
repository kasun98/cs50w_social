import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile

def index(request):
    posts = Post.objects.all().order_by('-datetime')
    if request.method == "POST":
        content = request.POST["new-post-ta"]
        poster_id = request.user
        post = Post.objects.create(
            poster_id = poster_id,
            content = content
        )
        messages.success(request, 'Post is published successfully!')
        return redirect("index")
    
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts":posts,
        'page_obj': page_obj
    })

def network(request):
    try:
        following = Profile.objects.get(profile_id=request.user).followings
        followings = Profile.objects.filter(profile_id__in=following)
        
        if len(followings) > 0 :
            return render(request, "network/network.html", {
                "followings":followings,
                })
        else:
            followings = None
            return render(request, "network/network.html", {
                "followings":followings})

    except:
        return redirect("index")


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
            profile = Profile.objects.create(profile_id=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def view_profile(request, uid):
    profile = get_object_or_404(Profile, profile_id=uid)
    posts =  Post.objects.filter(poster_id=uid).order_by('-datetime').all()
    followings = Profile.objects.get(profile_id=uid).fn_followings()
    followers = Profile.objects.get(profile_id=uid).fn_followers()
    if len(posts) > 0 :
        paginator = Paginator(posts, 10) # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        posts = None
        page_obj = None

    if request.user.id:
        follower = Profile.objects.get(profile_id=request.user).fn_followings(uid, "is_following")
    else:
        follower=None

    if request.method == "POST":  
        follow = Profile.objects.get(profile_id=request.user)
        account = Profile.objects.get(profile_id=uid)
        if follow.fn_followings(uid, "is_following") :
            follow.fn_followings(uid, "remove")
            account.fn_followers(request.user.id, "remove")
            follow.save()
            account.save()
            messages.success(request, f'Unfollowed {account.profile_id}!')
            return redirect("view_profile", uid)

        else:
            follow.fn_followings(uid, "append")
            account.fn_followers(request.user.id, "append")
            follow.save()
            account.save()
            messages.success(request, f'Following {account.profile_id}!')
            return redirect("view_profile", uid)
    
    return render(request, "network/profile.html", {
        "profile": profile,
        "posts":posts,
        'page_obj': page_obj,
        "follower": follower,
        "followings":followings,
        "followers":followers,
    })

def following_feed(request):
    try:
        followings = Profile.objects.get(profile_id=request.user).followings
        posts = Post.objects.filter(poster_id__in=followings).order_by('-datetime')

        if len(posts) > 0 :
            paginator = Paginator(posts, 10) # Show 10 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "network/index.html", {
                "posts":posts,
                'page_obj': page_obj})
        else:
            posts = None
            return render(request, "network/index.html", {
                "posts":posts})

    except:
        return redirect("index")

@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id = post_id, poster_id = request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required    
def likefn(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        
        data = json.loads(request.body)
        
        if data.get("like_count") >= 0:
            if data.get("likers"):
                post.likers = data["likers"]
            else:
                post.likers = []
            post.like_count = data["like_count"]
        post.save()
        return HttpResponse(status=204)

    # post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

