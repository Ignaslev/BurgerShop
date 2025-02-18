from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('menu/', views.menu, name='menu'),
    path('start-order/', views.start_order, name='start_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/finalize/', views.finalize_order, name='finalize_order'),
    path('order/success/', views.order_success, name='order_success'),

]
