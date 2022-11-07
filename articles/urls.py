from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path('create_cafe/', views.create_cafe, name='create_cafe'), #카페 생성
    path('<int:pk>/create_comment/', views.create_comment, name='create_comment'), #후기 생성
    path("<int:article_pk>/comments/<int:comment_pk>/delete/", views.comments_delete, name="comments_delete",), #후기 삭제
    path('<int:pk>/detail/', views.detail, name='detail'), #카페 디테일
    path('search/', views.search, name='search'), #검색 생성
    path('<int:pk>/like/', views.like, name='like'), #댓글공감
    path('<int:pk>/viewmore/', views.viewmore, name='viewmore'), #더보기
    path('<int:pk>/bookmark/', views.bookmark, name='bookmark'),
]


