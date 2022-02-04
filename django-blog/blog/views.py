from urllib import request
from webbrowser import get
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.template import context
from django.views.generic import *
from django.views.generic.base import View
from django.urls import reverse_lazy, resolve

from .models import Post, Comment


class IndexView(View):


    def get (self, request):
        """Return all published posts.(not including those set to be
    published in the future) and user info"""

        latest_post_list = Post.objects.order_by('-pub_date')[:5]
        return render(request, 'blog/index.html', {'latest_post_list' : latest_post_list})


class CreatePost(CreateView):

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdatePost(UpdateView):  
    model = Post
    fields = ['title', 'content']
    pk_url_kwarg = 'post_id'


class DeletePost(DeleteView):

    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')        


class CreateComment(CreateView):

    model = Comment
    fields = ['body']

    def form_valid(self, form):
        form.instance.name = self.request.user
        post_owner = Post.objects.filter(id = self.kwargs['post_id'])
        form.instance.post = post_owner[0]
        return super().form_valid(form)


class UpdateComment(UpdateView):  
    model = Comment
    fields = ['body']
    pk_url_kwarg = 'comment_id'


class DeleteComment(DeleteView):

    model = Comment 
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        postid = self.kwargs['post_id']
        return reverse_lazy('blog:post_details', kwargs={'post_id': postid})


# With this view, we can manage post details and comments
class DetailListView(ListView):

    paginate_by = 10
    template_name = 'blog/detail.html'
    context_object_name = 'comment_list'

    def get_queryset(self):
        self.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return Comment.objects.filter(post = self.post)

    
    def get_context_data(self, **kwargs ):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context  


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