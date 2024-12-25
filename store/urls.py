from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('user_edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('user_show/<int:user_id>', views.user_show, name='user_show'),
    path('shop/',views.shop,name='shop'),
    path('product_detail/<str:product_name>/',views.product_detail,name='product_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('shop_cart/',views.shop_cart,name='shop_cart'),
    path('about/',views.about,name='about'),  
    path('contact/',views.contact,name='contact'),  
]