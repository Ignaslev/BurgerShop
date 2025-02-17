from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('burger_shop/', include('burger_shop.urls')),
    path('', RedirectView.as_view(url='burger_shop/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
