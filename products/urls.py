from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('product/<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:category_slug>/', views.shop, name='category'),
]
