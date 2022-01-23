from django import views
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponseRedirect, request
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy

from .models import Post


class IndexView(View):


    def get (self, request):
        """Return all published posts.(not including those set to be
    published in the future) and user info"""

        latest_post_list = Post.objects.order_by('-pub_date')[:5]
        return render(request, 'blog/index.html', {'latest_post_list' : latest_post_list})


class CreatePost(generic.CreateView):

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeletePost(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class Details(generic.DetailView):

    model = Post
    template_name = 'blog/detail.html'

    


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