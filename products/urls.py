from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug>/',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/',views.remove_from_cart, name='remove_from_cart'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
]