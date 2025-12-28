from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:category_slug>/', views.shop, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='detail'),
]
