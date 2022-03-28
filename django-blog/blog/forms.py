from django import forms
from django.forms import ModelForm
from .models import Post, Comment, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, Fieldset
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineCheckboxes, Container
from django.utils.translation import gettext_lazy as _

# Customized authentication form that separates username and password validation


class CustomAuthenticationForm(AuthenticationForm):

    error_messages = {'invalid_login': _("Please enter a correct username"),
                      'invalid_password': _("Please enter a correct password"),
                      'inactive': _("This account is inactive."), }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username is not None:
            validate_user = self.check_user(username=username)
            if validate_user is None:
                raise self.get_invalid_user_error()

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is not None:
            validate_password = self.check_pass(password=password)
            if validate_password is None:
                raise self.get_invalid_password_error()

        return password

    def check_user(self, username):
        if User.objects.filter(username=username):
            return username
        return None

    def check_pass(self, password):
        # breakpoint()
        users = User.objects.all()
        for user in users:
            if user.check_password(password):
                return password
        return None

    def get_invalid_user_error(self):
        return ValidationError(
            # ahi que acceder al mensaje de error de alguna forma
            self.error_messages['invalid_login'],
            code='invalid_login',
        )

    def get_invalid_password_error(self):
        return ValidationError(
            self.error_messages['invalid_password'],
            code='invalid_password',
        )


# Login form
class LoginForm(CustomAuthenticationForm):

    remember_me = forms.BooleanField(required=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-authenticationForm"
        self.helper.form_class = "form-signin"
        self.helper.form_method = "post"
        self.helper.form_action = "login"
        self.helper.layout = Layout(


            Div( HTML("""{% load static %}<img class="mb-4" src="{% static 'images/logo.jpg' %}" >
                        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>"""),

            FloatingField("username", "password"),

            Div(
                Div(
                    Div("remember_me", css_class="checkbox mb-3"), css_class="col"),
                Div(HTML(
                    "<p><a href='{% url 'password_reset' %}'>Lost password?</a></p>"), css_class="col"),
                css_class="row"
            ),

            Submit('submit', 'Sign in', css_class="w-100 btn btn-lg btn-primary"),

            HTML("""<p class="mt-5 mb-3 text-muted">&copy; 2022 all rights deserved</p>"""), css_class="container"
            )
        )

        # self.helper.add_input(Submit('submit','Login'))


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
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
        fields = ('title', 'category', 'content', 'header_image',)

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
