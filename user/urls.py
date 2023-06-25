from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('orders/', views.orders, name='orders'),
    path('order_products/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.orderdetail, name='orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),

]