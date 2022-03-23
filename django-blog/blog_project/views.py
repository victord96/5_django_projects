from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from blog.forms import LoginForm
from django.contrib.auth.signals import user_logged_in

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
    form_class = LoginForm

    def form_valid(self, form):
        super().form_valid(form)

        """Security check complete. Log the user in."""
        #changed default login
        custom_login(self.request, form.get_user())

        #get remember me data from cleaned_data of form
        remember_me = form.cleaned_data['remember_me']  

        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is 
            self.request.session.modified = True

        return HttpResponseRedirect(self.get_success_url()) 