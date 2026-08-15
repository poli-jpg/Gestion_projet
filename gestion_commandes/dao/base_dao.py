from abc import ABC, abstractmethod
from gestion_commandes.database.connexion import DatabaseConnection


class BaseDAO(ABC):
    """Classe abstraite définissant les méthodes génériques pour tous les DAO."""

    def __init__(self):
        db = DatabaseConnection()
        self.conn = db.get_connexion()

    @abstractmethod
    def get_all(self):
        """Récupère tous les enregistrements."""
        return None

    @abstractmethod
    def get_by_id(self, identifiant):
        """Récupère un enregistrement par son ID."""
        return None

    @abstractmethod
    def delete(self, identifiant):
        """Supprime un enregistrement par son ID."""
        return None