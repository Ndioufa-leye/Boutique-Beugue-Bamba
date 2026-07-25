from django.contrib import admin
from .models import Produit, Commande, LigneCommande


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
   list_display = ('nom', 'prix', 'stock', 'created_at')
   search_fields = ('nom',)
   list_filter = ('created_at',)


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ['produit', 'nom_produit', 'prix_unitaire', 'quantite']
    can_delete = False


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom_client', 'telephone', 'total', 'date_commande']
    list_filter = ['date_commande']
    search_fields = ['nom_client', 'telephone']
    readonly_fields = ['date_commande']
    inlines = [LigneCommandeInline]