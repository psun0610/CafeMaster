
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Comment, Cafe
from .forms import CafeForm, CommentForm

# Create your views here.


def index(request):
    return render(request, "articles/index.html")



def create_cafe(request):
    if request.method == "POST":
        articleform = CafeForm(request.POST, request.FILES)
        if articleform.is_valid():
            article = articleform.save(commit=False)
            article.save()
        
            return redirect("articles:index")
    else:
        articleform = CafeForm()
    context = {"article_form": articleform}
    return render(request, "articles/create_cafe.html", context)

def create_comment(request):
    if request.method == "POST":
        commentForm = CommentForm(request.POST, request.FILES)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            
            comment.save()

            return redirect("articles:index")
    else:
        commentForm = CommentForm()
    context = {"article_form": commentForm}
    return render(request, "articles/create_comment.html", context)


