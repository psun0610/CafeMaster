from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path('create_cafe/', views.create_cafe, name='create_cafe'),#카페 생성
    path('<int:pk>/create_comment/', views.create_comment, name='create_comment'),#카페 생성
    path('<int:pk>/detail/', views.detail, name='detail'), #카페 디테일
    path('<int:pk>/like/', views.like, name='like'), #댓글공감
    path('viewmore/', views.viewmore, name='viewmore'), #더보기
]


