from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_post/', views.CreatePost.as_view(), name='new_post'),
    path('register/', views.Register, name='register'),
    path('<int:pk>/', views.Details.as_view(), name='detail'),
]