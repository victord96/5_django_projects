from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from blog.forms import LoginForm, CustomPasswordResetForm
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import render

def custom_login(request, user, backend=None):
    """
    modificated generic.auth login.
    Send signal with extra parameter: previous [session_key]
    """

    # get previous seesion_key for signal 
    prev_session_key = request.session.session_key

    #send extra argument prev_session_key 
    user_logged_in.send(sender=user.__class__, request=request, user=user, prev_session_key=prev_session_key)

class CustomLoginView(LoginView):
    # This allow us to show all our forms in template
    form_class = LoginForm

    # def get_context_data(self, **kwargs):
        
    #     if 'login_form' not in kwargs:
    #         kwargs['login_form'] = LoginForm()
    #     if 'password_reset_form' not in kwargs:
    #         kwargs['password_reset_form']  = CustomPasswordResetForm()
        
    #     return kwargs
        
    # def post(self, request, *args, **kwargs):
    # # This allow us to send response of all forms in our view
    #     ctxt = {}

    #     if 'login' in request.POST:
    #         login_form = LoginForm(request.POST)

    #         if not login_form.is_valid():
    #             ctxt['login_form'] = login_form

    #     elif 'password_reset' in request.POST:
    #         password_reset_form = CustomPasswordResetForm(request.POST)

    #         if not password_reset_form.is_valid():
    #             ctxt['password_reset_form'] = password_reset_form

    #     return render(request, self.template_name, self.get_context_data(**ctxt))

    def form_valid(self, form):
        #super().form_valid(form)

        """Security check complete. Log the user in."""
        #changed default login
        custom_login(self.request, form.get_user())

        #get remember me data from cleaned_data of form
        remember_me = form.cleaned_data['remember_me']  

        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is 
            self.request.session.modified = True

        return super().form_valid(form)

        #return HttpResponseRedirect(self.get_success_url()) 


    # def hide_form(self, **kwargs):
    #     #This method hide the password_reset_form on template
    #     document.getElementById("your form id").style.display="none";