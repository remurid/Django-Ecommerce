from django.urls import path

from . import views

urlpatterns = [

    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("vendor_account/", views.vendor_account, name='vendor_account'),
    path('vendor_account/vendor_profile/<int:pk>/', views.vendor_profile, name='vendor_profile'),
    path("vendor_account/vendor_products/", views.vendor_products, name='vendor_products'),
    path("vendor_account/vendors_orders/", views.vendors_orders, name='vendors_orders'),
    path("vendor_account/add_product/", views.add_product, name='add_product'),
    path("vendor_account/edit_product/<int:pk>/", views.edit_product, name='edit_product'),
    path("vendor_account/delete_product/<int:pk>/", views.delete_product, name='delete_product'),


]