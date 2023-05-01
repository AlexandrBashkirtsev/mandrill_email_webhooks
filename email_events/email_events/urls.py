"""
URL configuration for email_events project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('emailhooks.urls')),
    path('open/', include('notifications.urls'))
]
