from django.urls import path
from . import views
from accounts.views import chatbox
from accounts.views import delete_customer
from .views import customer_list
from .views import add_customer
from .views import update_customer
from .views import delete_order



urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),
    path('chatbox/', views.chatbox, name='chatbox'),
    path('dashboard/', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('customer/list/', customer_list, name='customer_list'),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('customer/update/<int:pk>/', views.update_customer, name='update_customer'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('delete_customer/<int:customer_id>/', delete_customer, name='delete_customer'),
     path('customer/add/', add_customer, name='add_customer'),
     path('customer/update/<int:pk>/', update_customer, name='update_customer'),
    path('create-customer/', views.create_customer, name='create_customer'),
    path('order/update/<int:pk>/', views.createOrder, name='update_order'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('order_list/', views.order_list, name='order_list'),
    #re_path(r'^.*$', home, name='home'),
]
