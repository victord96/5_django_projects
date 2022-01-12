from django import views
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponseRedirect, request
from django.views.generic.base import TemplateView, View

from .models import Post


class IndexView(View):


    def get (self, request):
        """Return all published posts.(not including those set to be
    published in the future) and user info"""

        latest_post_list = Post.objects.order_by('-pub_date')[:5]
        return render(request, 'blog/index.html', {'latest_post_list' : latest_post_list})


class CreatePost(generic.CreateView):

    template_name = 'blog/new_post.html'
    model = Post
    fields = ['title', 'content', 'pub_date']

    def post (self, request):
        
        return redirect('/blog')


class Details(generic.DetailView):

    model = Post
    template_name = 'blog/detail.html'

    def post(self):
    
        return Post.objects.all    


def Register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/blog/')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})