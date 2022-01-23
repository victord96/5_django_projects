from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.Register, name='register'),
    path('create_post/', views.CreatePost.as_view(), name='new_post'),
    path('<int:pk>/', views.Details.as_view(), name='post_detail'),  
    path('<int:pk>/delete_post/', views.DeletePost.as_view(), name='delete_post'),
 
]