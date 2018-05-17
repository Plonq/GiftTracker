from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .views import *

urlpatterns = [
    # Manually define URLs found in django.contrib.auth.urls so we can customise forms (needed for crispy-forms)
    # We use the default template names e.g. 'registration/<name>.html'
    path('login/', auth_views.LoginView.as_view(form_class=AuthenticationForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(form_class=PasswordChangeForm), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=SetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # URLs that aren't part of django auth
    path('register/', UserCreationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', UserActivationView.as_view(), name='activate_account'),
    path('profile/', UserProfileView.as_view(template_name='accounts/profile.html'), name='profile'),
    path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
    path('profile/edit/update-email/', UserEmailEditView.as_view(), name='email_edit'),
    path('verify-email/<uidb64>/<token>/', UserEmailVerificationView.as_view(), name='email_edit_verify'),
    path('delete/', UserDeleteAccountView.as_view(), name='delete_account'),
]
