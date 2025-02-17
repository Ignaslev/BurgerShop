from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('burger_shop/', include('burger_shop.urls')),
    path('', RedirectView.as_view(url='burger_shop/', permanent=True)),

]
