from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getProductData', views.getProductData, name='getProductData'),
    path('createFacture', views.createFacture, name='createFacture'),
    path('createLigneFacture', views.createLigneFacture, name='createLigneFacture'),
    #path('register', views.register, name='register'),
    #path('login', views.login, name='login'),
    #path('logout', views.logout, name='logout'),
    #path('dashboard', views.dashboard, name='dashboard'),
    #path('profile', views.profile, name='profile'),
]