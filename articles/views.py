
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
    user_tag = [('taste',request.user.taste),
                ('interior',request.user.interior),
                ('dessert',request.user.dessert)]
    reco = []
    for name,tag in user_tag:
        reco.append([name,tag])
    reco.sort(reverse=True)
    recommend = []
    for i in range(len(user_tag)):
        fir = Cafe.objects.order_by('-' + reco[i][0])[:2]
        list_ = []
        for cafe in fir:
            for comment in cafe.comment_set.all():
                if comment.picture != '':
                    list_.append((comment.picture, cafe))
                    break
        recommend.append(list_)
        adr = request.user.adress
        cafeadress = Cafe.objects.filter(adress=adr)
        cafeadr = cafeadress.order_by('-score')[:2]
        list_ = []
        for cafe in cafeadr:
            for comment in cafe.comment_set.all():
                if comment.picture != '':
                    list_.append((comment.picture, cafe))
                    break
        recommend.append(list_)
    print(recommend)
    

    context = {
        'swiper_lists': swiper_list,
        'recommend_lists' : recommend,
    }
    return render(request, "articles/index.html", context)



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


