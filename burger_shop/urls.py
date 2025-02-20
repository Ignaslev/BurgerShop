from django.urls import path
from . import views

app_name = 'burger_shop'

urlpatterns = [
    path('', views.index, name='homepage'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.get_user_profile, name='user-profile'),
    path('menu/', views.menu, name='menu'),
    path('start-order/', views.start_order, name='start_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/finalize/', views.finalize_order, name='finalize_order'),
    path('order/success/', views.order_success, name='order_success'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('create-burger/', views.create_burger, name='create_burger'),
    path('my-burgers/',views.user_burgers,name='user_burgers'),

    path('my-burgers/<int:burger_id>', views.get_user_burger, name='user_burger'),

]
