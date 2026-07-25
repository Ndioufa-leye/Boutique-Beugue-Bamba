from .panier import Panier

def panier_context(request):
    return {'panier_count': len(Panier(request))}