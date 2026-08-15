# models / commandes.py

class Commande:
    """Classe représentant une commande dans le système."""

    def __init__(self, numero, fournisseur_id, id=None, date_creation=None, statut="EN_ATTENTE"):
        self.id = id
        self.numero = numero
        self.fournisseur_id = fournisseur_id
        self.date_creation = date_creation
        self.statut = statut

    def __str__(self):
        return f"Commande ID: {self.id} | Numero: {self.numero} | Fournisseur ID: {self.fournisseur_id} | Statut: {self.statut}"

    def afficher(self):
        print(f"ID: {self.id}, Numero: {self.numero}, Fournisseur ID: {self.fournisseur_id}, Statut: {self.statut}, Date: {self.date_creation}")


class LigneCommande:
    """Classe représentant une ligne de commande."""

    def __init__(self, produit_id, quantite, prix_unitaire, id=None, commande_id=None):
        self.id = id
        self.commande_id = commande_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire

    def __str__(self):
        return f"Ligne ID: {self.id} | Produit ID: {self.produit_id} | Quantité: {self.quantite} | PU: {self.prix_unitaire}"