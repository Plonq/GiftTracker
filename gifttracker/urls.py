from django.contrib import admin
from django.urls import path, include


# Set django-admin names
admin.site.site_title = 'GiftTracker'
admin.site.site_header = 'GiftTracker Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    # Account related URLs. We don't namespace this, because we use built-in django auth views (which don't expect it)
    path('accounts/', include('accounts.urls')),
    # Main gift tracker urls
    path('', include('main.urls', namespace='main')),
]
