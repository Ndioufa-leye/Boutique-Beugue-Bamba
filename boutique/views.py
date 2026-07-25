from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Commande, LigneCommande



from django.db.models import Q
from .panier import Panier

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProduitForm
from .models import Produit

def liste_produits(request):
    query = request.GET.get('q', '').strip()
    produits = Produit.objects.all()
    if query:
        produits = produits.filter(
            Q(nom__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'boutique/liste_produits.html', {'produits': produits})


def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'boutique/detail_produit.html', {'produit': produit})


@staff_member_required
def creer_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'« {produit.nom} » a été créé avec succès.')
            return redirect('detail', pk=produit.pk)
    else:
        form = ProduitForm()
    return render(request, 'boutique/form_produit.html', {
        'form': form,
        'titre': 'Créer',
    })


@staff_member_required
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, f'« {produit.nom} » a été modifié.')
            return redirect('detail', pk=produit.pk)
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'boutique/form_produit.html', {
        'form': form,
        'titre': 'Modifier',
        'produit': produit,
    })


@staff_member_required
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        nom = produit.nom
        produit.delete()
        messages.success(request, f'« {nom} » a été supprimé.')
        return redirect('liste')
    return render(request, 'boutique/confirmer_suppr.html', {'produit': produit})

def ajouter_panier(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    panier = Panier(request)
    panier.ajouter(produit)
    messages.success(request, f'« {produit.nom} » a été ajouté au panier.')
    return redirect('liste')


def voir_panier(request):
    panier = Panier(request)
    return render(request, 'boutique/panier.html', {'panier': panier})


def supprimer_du_panier(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    panier = Panier(request)
    panier.supprimer(produit)
    messages.success(request, f'« {produit.nom} » a été retiré du panier.')
    return redirect('panier')


def vider_panier(request):
    panier = Panier(request)
    panier.vider()
    messages.success(request, 'Le panier a été vidé.')
    return redirect('panier')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Ton message a bien été envoyé ! Nous te répondrons rapidement.')
        return redirect('contact')
    return render(request, 'boutique/contact.html')


def a_propos(request):
    return render(request, 'boutique/a_propos.html')

def commande(request):
    panier = Panier(request)
    if len(panier) == 0:
        messages.warning(request, 'Ton panier est vide.')
        return redirect('liste')

    if request.method == 'POST':
        nouvelle_commande = Commande.objects.create(
            nom_client=request.POST.get('nom'),
            telephone=request.POST.get('telephone'),
            adresse=request.POST.get('adresse'),
            total=panier.get_total(),
        )

        for item in panier:
            LigneCommande.objects.create(
                commande=nouvelle_commande,
                produit=item['produit'],
                nom_produit=item['produit'].nom,
                prix_unitaire=item['prix'],
                quantite=item['quantite'],
            )
            # Décrémente le stock du produit
            produit = item['produit']
            produit.stock = max(produit.stock - item['quantite'], 0)
            produit.save()

        panier.vider()
        messages.success(request, f'Commande #{nouvelle_commande.id} confirmée ! Merci pour ta confiance.')
        return redirect('commande_confirmee', pk=nouvelle_commande.id)

    return render(request, 'boutique/commande.html', {'panier': panier})


def commande_confirmee(request, pk):
    cmd = get_object_or_404(Commande, pk=pk)
    return render(request, 'boutique/commande_confirmee.html', {'commande': cmd})

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Ton compte a été créé.')
            return redirect('liste')
    else:
        form = UserCreationForm()
    return render(request, 'boutique/inscription.html', {'form': form})