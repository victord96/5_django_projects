from django.urls import path, include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.AdminIndexView.as_view(), name='superindex'),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]