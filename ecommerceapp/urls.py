from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('profile', views.user_profile, name='user_profile'),
    path('myOrders/', views.myOrders, name='my_order'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),

]