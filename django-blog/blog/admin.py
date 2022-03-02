from django.contrib import admin
from .models import Category, Post, Comment, Profile

# Register your models here.  

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)