from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path('create_cafe/', views.create_cafe, name='create_cafe'),#카페 생성
    path('<int:pk>/create_comment/', views.create_comment, name='create_comment'),#카페 생성
    path('search/', views.search, name='search'),#검색 생성
]


