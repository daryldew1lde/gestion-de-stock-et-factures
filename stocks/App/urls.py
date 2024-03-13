from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getProductData', views.getProductData, name='getProductData'),
    path('createFacture', views.createFacture, name='createFacture'),
    path('createLigneFacture', views.createLigneFacture, name='createLigneFacture'),
    path('home_register', views.home_register, name='home_register'),
    path('home_login', views.home_login, name='home_login'),
    path('logout', views.logout, name='logout'),
    path('icons/', views.icons, name='icons'),
    path('user', views.user, name='user'),
    path('index', views.index, name='index'),
    path('user', views.user, name='user'),
    path('cat', views.cat, name='cat'),
    path('fact', views.fact, name='fact'),
    path('produits', views.produits, name='produits'),
    path('qr_code', views.qr_code, name='qr_code'),
    path('details_produit', views.details_produit, name='details_produit'),
    path('ajouter_produit', views.ajouter_produit, name='ajouter_produit'),
    path('modif_produit', views.modif_produit, name='modif_produit'),



]