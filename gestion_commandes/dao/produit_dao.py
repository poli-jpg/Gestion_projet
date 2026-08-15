from gestion_commandes.database.connexion import DatabaseConnection
from gestion_commandes.models.produit import Produit


class ProduitDAO:
    def __init__(self):
        db = DatabaseConnection()
        self.conn = db.get_connexion()

    def create(self, produit):
        """Ajoute un nouveau produit dans la base de données."""
        if not self.conn:
            return False

        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO produit (reference, designation, prix_unitaire, stock) 
                VALUES (%s, %s, %s, %s)
            """
            values = (produit.reference, produit.designation, produit.prix_unitaire, produit.stock)
            cursor.execute(query, values)

            self.conn.commit()
            print(" Produit ajouté avec succès !")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f" Erreur lors de l'ajout du produit : {e}")
            return False
        finally:
            cursor.close()

    def get_all(self):
        """Affiche la liste de tous les produits."""
        produits = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute("SELECT id, reference, designation, prix_unitaire, stock, date_creation FROM produit")
                rows = cursor.fetchall()
                for row in rows:
                    p = Produit(id=row[0], reference=row[1], designation=row[2],
                                prix_unitaire=row[3], stock=row[4], date_creation=row[5])
                    produits.append(p)
            except Exception as e:
                print(f" Erreur lors de la récupération des produits : {e}")
            finally:
                cursor.close()
        return produits

    def get_by_id_or_ref(self, identifiant):
        """Affiche les détails d'un produit (par ID ou référence)."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                if str(identifiant).isdigit():
                    query = "SELECT * FROM produit WHERE id = %s"
                else:
                    query = "SELECT * FROM produit WHERE reference = %s"

                cursor.execute(query, (identifiant,))
                row = cursor.fetchone()
                if row:
                    return Produit(id=row[0], reference=row[1], designation=row[2],
                                   prix_unitaire=row[3], stock=row[4], date_creation=row[5])
                else:
                    print(" Produit introuvable.")
            except Exception as e:
                print(f" Erreur : {e}")
            finally:
                cursor.close()
        return None

    def update(self, produit_id, nouvelle_designation, nouveau_prix, nouveau_stock):
        """Modifie un produit (prix, stock, désignation)."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = """
                    UPDATE produit 
                    SET designation = %s, prix_unitaire = %s, stock = %s 
                    WHERE id = %s
                """
                values = (nouvelle_designation, nouveau_prix, nouveau_stock, produit_id)
                cursor.execute(query, values)
                self.conn.commit()

                if cursor.rowcount > 0:
                    print(" Produit mis à jour avec succès !")
                else:
                    print(" Aucun produit n'a été modifié (ID introuvable).")
            except Exception as e:
                self.conn.rollback()
                print(f" Erreur lors de la mise à jour : {e}")
            finally:
                cursor.close()

    def delete(self, produit_id):
        """Supprime un produit (uniquement s'il n'apparaît dans aucune commande)."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM produit WHERE id = %s", (produit_id,))
                self.conn.commit()
                print(" Produit supprimé avec succès !")
            except Exception as e:
                self.conn.rollback()
                print(
                    f" Impossible de supprimer le produit. Il est probablement lié à une commande existante. (Erreur technique: {e})")
            finally:
                cursor.close()

    def search_by_designation(self, mot_cle):
        """Recherche des produits par désignation."""
        produits_trouves = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = "SELECT * FROM produit WHERE designation LIKE %s"
                cursor.execute(query, (f"%{mot_cle}%",))
                rows = cursor.fetchall()
                for row in rows:
                    p = Produit(id=row[0], reference=row[1], designation=row[2],
                                prix_unitaire=row[3], stock=row[4], date_creation=row[5])
                    produits_trouves.append(p)
            except Exception as e:
                print(f" Erreur de recherche : {e}")
            finally:
                cursor.close()
        return produits_trouves

    def get_alertes_stock(self, seuil):
        """Affiche les produits dont le stock est inférieur à un seuil."""
        produits_alerte = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = "SELECT * FROM produit WHERE stock < %s"
                cursor.execute(query, (seuil,))
                rows = cursor.fetchall()
                for row in rows:
                    p = Produit(id=row[0], reference=row[1], designation=row[2],
                                prix_unitaire=row[3], stock=row[4], date_creation=row[5])
                    produits_alerte.append(p)
            except Exception as e:
                print(f" Erreur lors de la récupération des alertes stock : {e}")
            finally:
                cursor.close()
        return produits_alerte