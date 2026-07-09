from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import ForumPost, ForumComment
from .forms import ForumPostForm, ForumCommentForm


@login_required
def forum_list(request):

    posts = ForumPost.objects.all().order_by("-created_at")

    return render(
        request,
        "forum/forum_list.html",
        {
            "posts": posts
        }
    )


@login_required
def create_post(request):

    if request.method == "POST":

        form = ForumPostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            # Assign the logged-in user
            post.author = request.user

            post.save()

            return redirect("forum_list")

    else:

        form = ForumPostForm()

    return render(
        request,
        "forum/create_post.html",
        {
            "form": form
        }
    )


@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        ForumPost,
        post_id=post_id
    )

    comments = ForumComment.objects.filter(
        post=post
    ).order_by("created_at")

    if request.method == "POST":

        form = ForumCommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post

            # Assign the logged-in user
            comment.author = request.user

            comment.save()

            return redirect(
                "post_detail",
                post_id=post.post_id
            )

    else:

        form = ForumCommentForm()

    return render(
        request,
        "forum/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form
        }
    )