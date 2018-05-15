from django.contrib import admin
from django.urls import path, include


# Set django-admin names
admin.site.site_title = 'GiftTracker'
admin.site.site_header = 'GiftTracker Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    # Rest of the auth URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # Main gift tracker urls
    path('', include('main.urls', namespace='main')),
]
