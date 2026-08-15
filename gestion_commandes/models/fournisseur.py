# models/fournisseur.py
class Fournisseur:
    """Classe représentant un fournisseur dans le système."""

    def __init__(self, code, raison_sociale, email, telephone, adresse, id=None, date_creation=None):
        self.id = id
        self.code = code
        self.raison_sociale = raison_sociale
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.date_creation = date_creation

    def __str__(self):
        return f"[{self.code}] {self.raison_sociale} - Tél: {self.telephone} | Email: {self.email}"


