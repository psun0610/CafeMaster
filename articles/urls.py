from django.urls import path 
from . import views

app_name = 'articles'

urlpatterns = [
  path('', views.index, name='index'), #기본페이지
  path('create/', views.create, name='create'),
  path('<int:pk>/', views.detail, name='detail'),
  path('<int:pk>/update/', views.update, name='update'), #수정
  path('<int:pk>/comments/', views.comment_create, name='comment_create'), #댓글
  path('<int:pk>/like/', views.like, name='like'),
]