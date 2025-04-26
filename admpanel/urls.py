from django.urls import path
from admpanel import views

urlpatterns = [
    path('adm-user/login', views.login_ad, name="login_ad"),
    path('adm/add-product', views.add_products, name='add_products'),
    path('adm/all-products', views.all_products, name='all_products'),
    path('adm/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('adm/update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('admin/all-orders/', views.admin_all_orders, name='admin_all_orders'),
    path('admin/order/mark-delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),


]
