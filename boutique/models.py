from django.db import models
class Produit(models.Model):
   nom = models.CharField(max_length=200)
   prix = models.DecimalField(max_digits=10, decimal_places=2)
   description = models.TextField()
   stock = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   image = models.ImageField(
      upload_to='produits/',
      null=True,
      blank=True
   )

   def __str__(self):
      return self.nom
   
   class Meta:
      ordering = ['-created_at'] # Trier les produits par date de création décroissante

class Commande(models.Model):
    nom_client = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    date_commande = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Commande #{self.id} - {self.nom_client}"

    class Meta:
        ordering = ['-date_commande']


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='lignes', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    nom_produit = models.CharField(max_length=200)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()

    def get_total(self):
        return self.prix_unitaire * self.quantite
      
      
