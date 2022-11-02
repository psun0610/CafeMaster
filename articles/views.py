
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Comment, Cafe
from .forms import CafeForm, CommentForm

# Create your views here.


def index(request):
    return render(request, "articles/index.html")



def create_cafe(request):
    if request.method == "POST":
        cafeform = CafeForm(request.POST, request.FILES)
        if cafeform.is_valid():
            cafe =cafeform.save(commit=False)
            cafe.save()
            return redirect("articles:index")
    else:
        cafeform = CafeForm()
    context = {"article_form":cafeform}
    return render(request, "articles/create_cafe.html", context)

def create_comment(request, pk):
    cafe = Cafe.objects.get(pk=pk)
    if request.method == "POST":
        commentForm = CommentForm(request.POST, request.FILES)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.cafe = cafe
            comment.user = request.user
            comment.save()
            return redirect("articles:index")
    else:
        commentForm = CommentForm()
    context = {"commentform": commentForm}
    return render(request, "articles/create_comment.html", context)


