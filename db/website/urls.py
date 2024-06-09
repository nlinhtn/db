from django.urls import path
from .views import product_list, add_product, delete_product, update_product
from .views import order_list, create_order, delete_order, create_booking, booking_list
from .views import dashboard

urlpatterns = [
    path("", product_list, name="product_list"),
    path("add_product/", add_product, name="add_product"),
    path("delete/<int:pk>", delete_product, name="delete_product"),
    path("update/<int:pk>", update_product, name="update_product"),
    path("order_list/", order_list, name="order_list"),
    path('create_order/', create_order, name='create_order'),
    path("delete_order/<int:pk>", delete_order, name="delete_order"),
    path("booking_list/", booking_list, name="booking_list"),
    path('create_booking/', create_booking, name='create_booking'),
    path("dashboard/", dashboard, name="dashboard" )
]
