from django.contrib import admin
from .models import User, Produit, Categorie, LigneFacture, Facture

class UserAdmin(admin.ModelAdmin):
    # Define the options and customizations for the User model
    list_display = ('username', 'email')
    search_fields = ["username", "email"]

class ProduitAdmin(admin.ModelAdmin):
    # Define the options and customizations for the Produit model
    list_display = ["id", "nom", "categorie", "prix_unitaire", "stock"]
    list_filter = ["categorie"]
    search_fields = ["nom", "description"]
    
class CategorieAdmin(admin.ModelAdmin):
    # Define the options and customizations for the Categorie model
    list_display = ["id", "nom", "description"]
    search_fields = ["nom", "description"]

class FactureAdmin(admin.ModelAdmin):
    # Define the options and customizations for the Facture model
    list_display = ["id", "date", "total"]

class LigneFactureAdmin(admin.ModelAdmin):
    # Define the options and customizations for the LigneFacture model
    list_display = ["id", "produit", "facture", "quantite", "prix_unitaire", "total"]
    
# Register the models with their corresponding ModelAdmin classes
admin.site.register(User, UserAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(LigneFacture, LigneFactureAdmin)
admin.site.register(Facture, FactureAdmin)
