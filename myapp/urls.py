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
    path('color_filter', views.color_filter, name='color_filter'),
    path('size_filter', views.size_filter, name='size_filter'),
    path('price_filter', views.price_filter, name='price_filter'),
    path("view_details", views.view_details, name="view_details"),
    path("search", views.search, name="search"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("save_review", views.save_review, name="save_review"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    # path("cart_view", views.cart_view, name="cart_view"),
    path("latest_products", views.latest_products, name="latest_products"),
    path("popular_products", views.popular_products, name="popular_products"),
    path("best_rated_products", views.best_rated_products, name="best_rated_products"),

]
