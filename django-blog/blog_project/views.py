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
        """Security check complete. Log the user in."""

        # changed default login
        custom_login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url()) 