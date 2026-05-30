from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
    path('', RedirectView.as_view(url='/projects/list/', permanent=False)),  # редирект / → /projects/list/
]

if settings.DEBUG:
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 