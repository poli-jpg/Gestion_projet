import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gestion_commandes.database.config import TYPE_BD
from gestion_commandes.database.connexion import DatabaseConnection


def creer_les_tables():
    db = DatabaseConnection()
    conn = db.get_connexion()

    if conn:
        cursor = conn.cursor()
        try:
            # ===================== TABLE FOURNISSEUR =====================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fournisseur (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(50) NOT NULL UNIQUE,
                    raison_sociale VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    telephone VARCHAR(30) NOT NULL,
                    adresse VARCHAR(50) NOT NULL,
                    date_creation DATE DEFAULT (CURRENT_DATE)
                )
            """)
            print(" Table 'fournisseur' vérifiée/créée.")

            # ===================== TABLE PRODUIT=====================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produit (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(50) NOT NULL UNIQUE,
                    designation VARCHAR(50) NOT NULL,
                    prix_unitaire DECIMAL(10, 2) CHECK (prix_unitaire > 0),
                    stock INT NOT NULL CHECK (stock >= 0),
                    date_creation DATE DEFAULT (CURRENT_DATE)
                )
            """)
            print(" Table 'produit' vérifiée/créée.")

            # ===================== TABLE COMMANDE =====================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commande (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numero VARCHAR(50) NOT NULL UNIQUE,
                    date_commande DATE DEFAULT (CURRENT_DATE),
                    fournisseur_id INT,
                    montant_total DECIMAL(10, 2) DEFAULT 0.0,
                    statut VARCHAR(50) NOT NULL DEFAULT 'EN_ATTENTE',
                    date_creation DATE DEFAULT (CURRENT_DATE),
                    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id)
                )
            """)
            print(" Table 'commande' vérifiée/créée.")

            # ===================== TABLE LIGNE COMMANDE =====================

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ligne_commande (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    commande_id INT,
                    produit_id INT,
                    quantite INT NOT NULL CHECK (quantite > 0),
                    prix_unitaire DECIMAL(10, 2),
                    FOREIGN KEY (commande_id) REFERENCES commande(id) ON DELETE CASCADE,
                    FOREIGN KEY (produit_id) REFERENCES produit(id) ON DELETE RESTRICT
                )
            """)
            print("     Table 'ligne_commande' vérifiée/créée.")

            conn.commit()
            print("Toutes les tables ont été créées avec succès !")

        except Exception as e:
            conn.rollback()
            print(f"  Erreur lors de la création des tables : {e}")
        finally:
            cursor.close()
            db.disconnect()


if __name__ == "__main__":
    print(f"Initialisation de la base de données ({TYPE_BD})...")
    creer_les_tables()