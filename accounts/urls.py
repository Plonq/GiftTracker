from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .views import UserCreationView, UserActivationView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    # Override django auth templates with our own
    path('login/', LoginView.as_view(form_class=AuthenticationForm, redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change_form.html', form_class=PasswordChangeForm)),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html')),
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html', form_class=PasswordResetForm)),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html')),
    re_path(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=SetPasswordForm)),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html')),

    # Fall back on defaults for everything else
    path('', include('django.contrib.auth.urls')),

    # Other accounts-related pages not included in django auth
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', UserActivationView.as_view(), name='activate_account'),
    path('register/', UserCreationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('profile/edit/update-email/', views.update_email, name='update_email'),
    # re_path('^profile/edit/update-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', views.update_email_verify, name='update_email_verify'),
    # path('delete/', views.delete_account, name='delete_account'),
    # path('disable/', views.disable_account, name='disable_account'),
]
