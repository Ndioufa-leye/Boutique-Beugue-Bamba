from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_produits, name='liste'),
    path('produits/', views.liste_produits, name='liste'),
    path('produit/<int:pk>/', views.detail_produit, name='detail'),
    path('creer/', views.creer_produit, name='creer'),
    path('modifier/<int:pk>/', views.modifier_produit, name='modifier'),
    path('supprimer/<int:pk>/', views.supprimer_produit, name='supprimer'),

    path('panier/', views.voir_panier, name='panier'),
    path('panier/ajouter/<int:pk>/', views.ajouter_panier, name='ajouter_panier'),
    path('panier/supprimer/<int:pk>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('commande/', views.commande, name='commande'),
    path('commande/<int:pk>/confirmee/', views.commande_confirmee, name='commande_confirmee'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', auth_views.LoginView.as_view(template_name='boutique/connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(next_page='liste'), name='deconnexion'),
]