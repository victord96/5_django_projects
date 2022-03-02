from django import forms
from django.forms import ModelForm
from .models import Post, Comment, Profile
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }        


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category' , 'content', 'header_image',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }  


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'title': 'Write Something'})
        }        