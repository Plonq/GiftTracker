from django.shortcuts import render, HttpResponse
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import UserCreationForm
from .models import User


class UserCreationView(View):
    """
    User registration
    """
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    done_template_name = 'accounts/register_done.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user_obj = form.save()

            # Create activation URL
            kwargs = {
                "uidb64": urlsafe_base64_encode(force_bytes(user_obj.pk)).decode(),
                "token": default_token_generator.make_token(user_obj)
            }
            activation_url = reverse('accounts:activate_account', kwargs=kwargs)
            activation_url_full = '{0}://{1}{2}'.format(request.scheme, request.get_host(), activation_url)
            user_obj.send_email(
                subject='Activate your account',
                message='Dear {0},\n\nThank you for registering with GiftTracker. Please activate your account by clicking the below link.\n\n{1}'.format(user_obj.get_short_name(), activation_url_full),
            )

            return render(request, self.done_template_name)


class UserActivationView(View):
    """
    Activates an account using provided token and user id
    """
    template_name = 'accounts/activation_done.html'

    def get(self, request, uidb64, token):
        try:
            # Decode user ID and get user from DB
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user and default_token_generator.check_token(user, token):
            # Activate the user and display success page
            user.is_active = True
            user.save()
            return render(request, self.template_name)
        else:
            return HttpResponse("Activation link has expired")


class UserProfileView(View):
    """
    Displays user account information
    """
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name)
