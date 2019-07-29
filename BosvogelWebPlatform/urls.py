from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('agenda/', include('apps.agenda.urls')),
                  path('profile/', include('apps.profile.urls')),
                  path('verhuur/', include('apps.rent.urls')),
                  path('', include('apps.home.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
