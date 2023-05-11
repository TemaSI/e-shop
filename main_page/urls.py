from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('category/<int:pk>/', views.get_exact_categeory),
    path('item/<int:pk>/', views.exact_product),
    path('cart', views.get_user_cart),
    path('order', views.complete_order)

]