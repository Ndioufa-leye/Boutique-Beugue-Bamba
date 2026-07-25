from django import forms

from .models import Produit


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'prix', 'description', 'stock', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nom': 'Nom',
            'prix': 'Prix (€)',
            'stock': 'Quantité en stock',
            'image': 'Photo du produit',
        }
