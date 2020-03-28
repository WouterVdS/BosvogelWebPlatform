from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('agenda/', include('apps.agenda.urls')),
                  path('leiding/', include('apps.leiding.urls')),
                  path('verhuur/', include('apps.rent.urls')),
                  path('takken/', include('apps.takken.urls')),
                  path('', include('apps.home.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
