from decimal import Decimal
from .models import Produit


class Panier:
    def __init__(self, request):
        self.session = request.session
        panier = self.session.get('panier')
        if not panier:
            panier = self.session['panier'] = {}
        self.panier = panier

    def ajouter(self, produit, quantite=1):
        produit_id = str(produit.id)
        if produit_id in self.panier:
            self.panier[produit_id]['quantite'] += quantite
        else:
            self.panier[produit_id] = {
                'quantite': quantite,
                'prix': str(produit.prix),
            }
        self.sauvegarder()

    def sauvegarder(self):
        self.session.modified = True

    def supprimer(self, produit):
        produit_id = str(produit.id)
        if produit_id in self.panier:
            del self.panier[produit_id]
            self.sauvegarder()

    def vider(self):
        self.session['panier'] = {}
        self.sauvegarder()

    def __iter__(self):
        produit_ids = self.panier.keys()
        produits = Produit.objects.filter(id__in=produit_ids)
        panier = self.panier.copy()
        for produit in produits:
            panier[str(produit.id)]['produit'] = produit

        for item in panier.values():
            item['prix'] = Decimal(item['prix'])
            item['total'] = item['prix'] * item['quantite']
            yield item

    def __len__(self):
        return sum(item['quantite'] for item in self.panier.values())

    def get_total(self):
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.panier.values())