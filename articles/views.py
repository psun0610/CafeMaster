
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Comment, Cafe
from .forms import CafeForm, CommentForm

# Create your views here.


def index(request):
    # 해시태그 탑9 사진과 카페정보
    goods = (
    (1,'taste'),
    (2,'interior'),
    (3,'dessert'),
    )
    swiper_list = []
    for num, good in goods:
        list_ = []
        for cafe in Cafe.objects.order_by('-' + good)[:9]:
            for comment in cafe.comment_set.all():
                if comment.picture != '':
                    list_.append((comment.picture, cafe))
                    break
        swiper_list.append(list_)

    # 사용자 추천 카페 정보
    recommend = []
    adr = request.user.area
    cafeaddress = Cafe.objects.filter(address=adr)
    cafeadr = cafeaddress.order_by('-score')[:2]
    for cafe in cafeadr:
        for comment in cafe.comment_set.all():
            if comment.picture != '':
                recommend.append((comment.picture, cafe))
                break

    user_tag = [('taste', request.user.taste),
                ('interior', request.user.interior),
                ('dessert', request.user.dessert)]
    reco = sorted(user_tag, reverse=True, key=lambda x:x[1])
    for i in range(len(user_tag)):
        fir = Cafe.objects.order_by('-' + reco[i][0])[:2]
        for cafe in fir:
            for comment in cafe.comment_set.all():
                if comment.picture != '':
                    recommend.append((comment.picture, cafe))
                    break
    print(recommend)
    
    # 가까운 카페
    closecafe = []
    adr = request.user.area
    cafeaddress = Cafe.objects.filter(address=adr)
    cafeadr = cafeaddress.order_by('-score')[2:6]
    for cafe in cafeadr:
        for comment in cafe.comment_set.all():
            if comment.picture != '':
                closecafe.append((comment.picture, cafe))
                break
    
    # 후기가 많은 카페
    commentcafe = []
    cafes = Cafe.objects.order_by('-comment_count')[:4]
    for cafe in cafes:
        for comment in cafe.comment_set.all():
            if comment.picture != '':
                commentcafe.append((comment.picture, cafe))
                break

    context = {
        'swiper_lists': swiper_list,
        'recommend_lists' : recommend,
        'closecafe_lists' : closecafe,
        'commentcafe_lists' : commentcafe,
    }
    return render(request, "articles/index.html", context)

def detail(request, pk):
    return render(request, "articles/detail.html")

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
            if '1' in comment.tag:
                cafe.taste = cafe.taste + 1
                cafe.score = cafe.score + 1
                print(cafe.taste)
            if '2' in comment.tag:
                cafe.interior = cafe.interior + 1
                cafe.score = cafe.score + 1
            if '3' in comment.tag:
                cafe.dessert = cafe.dessert + 1
                cafe.score = cafe.score + 1
            cafe.save()
            comment.save()
            return redirect("articles:index")
    else:
        commentForm = CommentForm()
    context = {"commentform": commentForm}
    return render(request, "articles/create_comment.html", context)

def search(request):
    pass