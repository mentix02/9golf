from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api')),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
