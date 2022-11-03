
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Comment, Cafe
from .forms import CafeForm, CommentForm
from django.db.models import Q
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
        for cafe in Cafe.objects.order_by('-' + good)[:9]:
            swiper_list.append(cafe)
        

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
        for cafe in  Cafe.objects.order_by('-' + reco[i][0])[:2]:
            recommend.append(cafe)
    
    # 가까운 카페
    adr = request.user.area
    cafeaddress = Cafe.objects.filter(address=adr)
    closecafe = cafeaddress.order_by('-score')[2:6]

        
    
    # 후기가 많은 카페
    commentcafe = Cafe.objects.order_by('-pk')[:4]

    context = {
        'swiper_list': swiper_list,
        'recommend_list' : recommend,
        'commentcafe_list' : closecafe,
        'commentcafe_list' : commentcafe,
    }
    return render(request, "articles/index.html", context)

# 카페 상세정보
def detail(request, pk):
    cafe = Cafe.objects.get(pk=pk)
    comment_form = CommentForm()
    cafe.score = cafe.taste + cafe.interior + cafe.dessert
    cafe.save()
    context = {
        'cafe': cafe,
        'comment' : cafe.comment_set.all(),
        }
    return render(request, "articles/detail.html", context)

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
    if 'searchs' in request.GET:
        query = request.GET.get('searchs')
        cafes = Cafe.objects.all().filter(
            Q(name__icontains=query) |
            Q(address__icontains=query)
        )
    context = {
        'query': query,
        'cafes': cafes,
    }
    return render(request, 'articles/search.html', context)

from django.http import JsonResponse
def like(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.user in comment.like.all():
        comment.like.remove(request.user)
        is_liked = False
    else:
        comment.like.add(request.user)
        is_liked = True
    
    context = {'isLiked': is_liked, 'likeCount': comment.like.count()}
    return JsonResponse(context)

def viewmore(request):
    # 사용자 추천 카페 정보
    recommend = []
    adr = request.user.area
    cafeaddress = Cafe.objects.filter(address=adr)
    cafeadr = cafeaddress.order_by('-score')[:2]
    for cafe in cafeadr:
        recommend.append(cafe)

    
    user_tag = [('taste', request.user.taste),
                ('interior', request.user.interior),
                ('dessert', request.user.dessert)]
    reco = sorted(user_tag, reverse=True, key=lambda x:x[1])
    for i in range(len(user_tag)):
        fir = Cafe.objects.order_by('-' + reco[i][0])[:2]
        for cafe in fir:
            recommend.append(cafe)
            
    reco = sorted(user_tag, reverse=True, key=lambda x:x[1])
    for i in range(len(user_tag)):
        fir = Cafe.objects.order_by('-' + reco[i][0])[2:6]
        for cafe in fir:
            recommend.append(cafe)
    
    # 가까운 카페
    
    adr = request.user.area
    cafeaddress = Cafe.objects.filter(address=adr)
    closecafe = cafeaddress.order_by('-score')[:20]
    
                
    
    # 후기가 많은 카페
    commentcafe = Cafe.objects.order_by('-pk')[:20]

    context = {
        'recommend' : recommend,
        'closecafe' : closecafe,
        'commentcafe' : commentcafe,
    }
    return render(request, "articles/viewmore.html", context)

