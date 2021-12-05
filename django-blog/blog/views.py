from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'


    def get_queryset(self):
        """Return all published posts.(not including those set to be
    published in the future)"""
        
        return Post.objects.order_by('-pub_date')[:5]


#def create_post(request, post_id):

