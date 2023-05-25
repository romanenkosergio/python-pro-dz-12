from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post


def get_cache_key(post_id):
    cache_key = f"post_{post_id}"
    return cache_key


def clear_post_cache(post_id):
    cache_key = get_cache_key(post_id)
    cache.delete(cache_key)


def home(request):
    """Home page."""
    return render(request, "posts/home.html")


def posts_list(request):
    """List of posts."""
    posts = Post.objects.all()
    return render(request, "posts/list.html", {"posts": posts})


def post_create(request):
    """Create a new post."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if not form.is_valid():
            return redirect("post_create")
        form.save()
        return redirect("posts_list")
    else:
        form = PostForm()
        return render(request, "posts/create.html", {"form": form})


def post_edit(request, id):
    """Edit post"""
    try:
        current_post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return redirect("posts_list")

    cache_key = get_cache_key(id)
    cached_data = cache.get(cache_key)

    if request.method == "POST":
        form = PostForm(request.POST, instance=current_post)
        if form.is_valid():
            form.save()
            clear_post_cache(id)
            return redirect("posts_list")
    else:
        form = PostForm(instance=current_post)

    if cached_data is not None:
        return HttpResponse(cached_data)

    html = render(request, "posts/edit.html", {"post": current_post, "form": form}).content
    cache.set(cache_key, html)

    return render(request, "posts/edit.html", {"post": current_post, "form": form})


def post_delete(request, id):
    """Delete post."""
    try:
        current_post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return redirect("posts_list")

    if request.method == "POST":
        current_post.delete()
        return redirect("posts_list")
    else:
        return render(request, "posts/delete.html", {"post": current_post})
