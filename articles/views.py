
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
    (4,'emotion'),
    (5,'hip'),
    (6,'study'),
    (7,'love'),
    (8,'sight'),
    )
    swiper_list = []
    for num, good in goods:
        for cafe in Cafe.objects.order_by('-' + good)[:9]:
            swiper_list.append(cafe)
        

    # 사용자 추천 카페 정보
    if request.user.is_authenticated: 
        recommend = []
        adr = request.user.area
        cafeaddress = Cafe.objects.filter(address=adr)
        cafeadr = cafeaddress.order_by('-score')[:4]
        for cafe in cafeadr:
            for comment in cafe.comment_set.all():
                if comment.picture != '':
                    recommend.append((comment.picture, cafe))
                    break

        user_tag = [('taste', request.user.taste),
                    ('interior', request.user.interior),
                    ('dessert', request.user.dessert),
                    ('emotion',  request.user.emotion),
                    ('hip',  request.user.hip),
                    ('study',  request.user.study),
                    ('love',  request.user.love),
                    ('sight',  request.user.sight),
                    ]
        reco = sorted(user_tag, reverse=True, key=lambda x:x[1])
        for i in range(len(user_tag)):
            for cafe in  Cafe.objects.order_by('-' + reco[i][0])[:1]:
                recommend.append(cafe)
    else:
        recommend = Cafe.objects.order_by('-score')[:12]
    
    # 가까운 카페
    if request.user.is_authenticated:
        adr = request.user.area
        cafes = Cafe.objects.all()
        closecafe = []
        for cafe in cafes:
            if adr in cafe.address:
                closecafe.append(cafe)
                if len(closecafe)==4:
                    break
    else:
        adr = '서울'
        cafes = Cafe.objects.all()
        closecafe = []
        for cafe in cafes:
            if adr in cafe.address:
                closecafe.append(cafe)
                if len(closecafe)==4:
                    break
    
    # 후기가 많은 카페
    commentcafe = Cafe.objects.order_by('-pk')[:4]

    context = {
        'swiper_list': swiper_list,
        'recommend_list' : recommend,
        'closecafe_list' : closecafe,
        'commentcafe_list' : commentcafe,
    }
    return render(request, "articles/index.html", context)

# 카페 상세정보
def detail(request, pk):
    cafe = Cafe.objects.get(pk=pk)
    goods = (
        (cafe.taste,'커피가맛있는'),
        (cafe.interior,'인테리어가예쁜'),
        (cafe.dessert,'디저트가맛있는'),
        (cafe.emotion,'감성충만한'),
        (cafe.hip,'힙한'),
        (cafe.study,'집중하기좋은'),
        (cafe.love,'데이트하기좋은'),
        (cafe.sight,'뷰가좋은'),
    )
    comment_form = CommentForm()
    cafe.score = cafe.taste + cafe.interior + cafe.dessert
    cafe.save()
    tag = []
    for good,name in goods:
        li = []
        li.append(good)
        li.append(name)
        tag.append(li)
    tag = sorted(tag, reverse=True, key=lambda x:x[0])
    hashtag = []
    for i in range(3):
        hashtag.append(tag[i][1])
    context = {
        'cafe': cafe,
        'comment' : cafe.comment_set.all(),
        'hashtag' : hashtag,
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
            if '4' in comment.tag:
                cafe.emotion = cafe.emotion + 1
                cafe.score = cafe.score + 1
            if '5' in comment.tag:
                cafe.hip = cafe.hip + 1
                cafe.score = cafe.score + 1
            if '6' in comment.tag:
                cafe.study = cafe.study + 1
                cafe.score = cafe.score + 1
            if '7' in comment.tag:
                cafe.love = cafe.love + 1
                cafe.score = cafe.score + 1
            if '8' in comment.tag:
                cafe.sight = cafe.sight + 1
                cafe.score = cafe.score + 1
            cafe.save()
            comment.save()
            return redirect("articles:detail", pk)
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

def viewmore(request, pk):
    
    if request.user.is_authenticated:
        if pk == 1:
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
            
            context = {
            'recommend' : recommend,
            }
            return render(request, "articles/viewmore(re).html", context) 

    else:
        if pk == 1:
            recommend = Cafe.objects.order_by('-score')[:20]
            context = {
                'recommend' : recommend,
            }
            return render(request, "articles/viewmore(re).html", context)    
    

    # 가까운 카페
    if request.user.is_authenticated:
        if pk == 2:
            
            adr = request.user.area
            cafes = Cafe.objects.all()
            closecafe = []
            for cafe in cafes:
                if adr in cafe.address:
                    closecafe.append(cafe)
                    if len(closecafe)==20:
                        break
                    else:
                        continue

            context = {
                'closecafe' : closecafe,
            }
            return render(request, "articles/viewmore(cl).html", context)   

    else:
        if pk == 2:
            adr = '서울'
            cafes = Cafe.objects.all()
            closecafe = []
            for cafe in cafes:
                if adr in cafe.address:
                    closecafe.append(cafe)
                    if len(closecafe)==20:
                        break
                    else:
                        continue


            context = {
                'closecafe' : closecafe,
            }
            return render(request, "articles/viewmore(cl).html", context)   
                
    
    # 후기가 많은 카페
    if pk == 3:
        commentcafe = Cafe.objects.order_by('-pk')[:20]

        context = {
            'commentcafe' : commentcafe,
        }
        return render(request, "articles/viewmore(co).html", context)

def bookmark(request, pk):
    cafe = Cafe.objects.get(pk=pk)
    if request.user in cafe.bookmarks.all():
        cafe.bookmarks.remove(request.user)
        marked = False
    else:
        cafe.bookmarks.add(request.user)
        marked = True
    
    context = {'marked': marked}
    return JsonResponse(context)