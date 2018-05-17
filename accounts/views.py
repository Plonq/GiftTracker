from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserCreationForm, UserProfileEditForm, EmailChangeForm
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
            activation_url = reverse('activate_account', kwargs=kwargs)
            activation_url_full = '{0}://{1}{2}'.format(request.scheme, request.get_host(), activation_url)
            user_obj.send_email(
                subject='Activate your account',
                message='Dear {0},\n\nThank you for registering with GiftTracker.\nPlease activate your account by clicking the link below.\n\n{1}'.format(user_obj.get_short_name(), activation_url_full),
            )

            return render(request, self.done_template_name)
        else:
            return render(request, self.template_name, {'form': form})


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


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class UserProfileEditView(LoginRequiredMixin, View):
    """
    Allows user to edit account information (profile)
    """
    form_class = UserProfileEditForm
    template_name = 'accounts/profile_edit_form.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, self.template_name, {'form': form})


class UserEmailEditView(LoginRequiredMixin, View):
    """
    Allow user to update their email address, requiring verification
    """
    form_class = EmailChangeForm
    template_name = 'accounts/email_edit_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            # Send verification email
            kwargs = {
                "uidb64": urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
                "token": default_token_generator.make_token(request.user)
            }
            verification_url = reverse("email_edit_verify", kwargs=kwargs)
            verification_url_full = "{0}://{1}{2}".format(request.scheme, request.get_host(), verification_url)
            request.user.send_email(
                subject='Verify Email Address',
                message='Dear {0},\n\nPlease verify your email address by clicking the link below.\n\n{1}'.format(request.user.get_short_name(), verification_url_full),
            )
            return render(request, 'accounts/email_edit_done.html')
        else:
            return render(request, self.template_name, {'form': form})


class UserEmailVerificationView(LoginRequiredMixin, View):
    """
    Verifies a new email address for existing user
    """
    template_name = 'accounts/email_edit_complete.html'

    def get(self, request, uidb64, token):
        try:
            # Decode user ID and get user from DB
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user and default_token_generator.check_token(user, token):
            # Get new email address from user object and replace actual email
            if user.requested_email:
                user.email = user.requested_email
                user.requested_email = None
                user.save()
                return render(request, self.template_name)
            else:
                return HttpResponse("Verification link is invalid")
        else:
            return HttpResponse("Verification link has expired")


class UserDeleteAccountView(LoginRequiredMixin, View):
    """
    Deletes a user's own account
    """
    template_name = 'accounts/account_delete_confirm.html'
    success_template_name = 'accounts/account_delete_complete.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST['confirm'] == '1':
            request.user.delete()
            return render(request, self.success_template_name)
        return redirect('main:home')
