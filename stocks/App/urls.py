from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getProductData', views.getProductData, name='getProductData'),
    path('createFacture', views.createFacture, name='createFacture'),
    path('createLigneFacture', views.createLigneFacture, name='createLigneFacture'),
    path('home_register', views.home_register, name='home_register'),
    path('home_login', views.home_login, name='home_login'),
    path('logout', views.logout_view, name='logout'),
    path('icons/', views.icons, name='icons'),
    path('suppruser', views.suppruser, name='suppruser'),
    path('user', views.user, name='user'),
    path('index', views.index, name='index'),
    path('modif_user', views.modif_user, name='modif_user'),
    path('user', views.user, name='user'),
    path('suppr_produit', views.suppr_produit, name='suppr'),
    path('suppr_cat', views.suppr_cat, name='suppr_cat'),
    path('suppr_fact', views.suppr_fact, name='supprfact'),
    path('cat', views.cat, name='cat'),
    path('details_fact', views.details_fact, name='details_fact'),
    path('fact', views.fact, name='fact'),
    path('createuser', views.createuser, name='createuser'),
    path('produits', views.produits, name='produits'),
    path('qr_code', views.qr_code, name='qr_code'),
    path('details_produit', views.details_produit, name='details_produit'),
    path('ajouter_produit', views.ajouter_produit, name='ajouter_produit'),
    path('modif_produit', views.modif_produit, name='modif_produit'),



]