"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('logout/', views.logout_view, name='logout'),
    path('contact', views.contact, name='contact'),
    path('detail', views.detail, name='detail'),
    path('shop', views.shop, name='shop'),
    path('color_filter', views.color_filter, name="color_filter"),
    path('size_filter', views.size_filter, name="size_filter"),
    path('price_filter', views.price_filter, name="price_filter"),
    path("view_details", views.view_details, name="view_details"),
    path("search", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login", views.login, name="login"),
    path("forgot_password",views.forgot_password,name="forgot_password"),
    path("send_otp/",views.send_otp,name="send_otp"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("save_review", views.save_review, name="save_review"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("plus_cart", views.plus_cart, name="plus_cart"),
    path("minus_cart", views.minus_cart, name="minus_cart"),
    path("remove_cart", views.remove_cart, name="remove_cart"),
    path("latest_products", views.latest_products, name="latest_products"),
    path("popular_products", views.popular_products, name="popular_products"),
    path("best_rated_products", views.best_rated_products, name="best_rated_products"),
    path("add_billing_address", views.add_billing_address, name="add_billing_address"),
    path("Order", views.Order, name="Order"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("add_wishlist", views.add_wishlist, name="add_wishlist"),
    path("remove_wishlist", views.remove_wishlist, name="remove_wishlist"),
    path('profile',views.profile,name="profile"),
    path('update_profile',views.update_profile,name="update_profile"),
    path('upload_profile_image', views.upload_profile_image, name='upload_profile_image'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    path('send_message',views.send_message,name='send_message'),

]
