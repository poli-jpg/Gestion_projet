
from gestion_commandes.database.connexion import DatabaseConnection
from gestion_commandes.models.fournisseur import Fournisseur


class FournisseurDAO:
    def __init__(self):
        db = DatabaseConnection()
        self.conn = db.get_connexion()

    def create(self, fournisseur):
        """Ajoute un nouveau fournisseur dans la base de données."""
        if not self.conn:
            return False

        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO fournisseur (code, raison_sociale, email, telephone, adresse) 
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (fournisseur.code, fournisseur.raison_sociale, fournisseur.email,
                      fournisseur.telephone, fournisseur.adresse)
            cursor.execute(query, values)

            self.conn.commit()
            print(" Fournisseur ajouté avec succès !")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f" Erreur lors de l'ajout du fournisseur : {e}")
            return False
        finally:
            cursor.close()

    def get_all(self):
        """Afficher la liste de tous les fournisseurs."""
        fournisseurs = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    "SELECT id, code, raison_sociale, email, telephone, adresse, date_creation FROM fournisseur")
                rows = cursor.fetchall()
                for row in rows:
                    f = Fournisseur(id=row[0], code=row[1], raison_sociale=row[2],
                                    email=row[3], telephone=row[4], adresse=row[5], date_creation=row[6])
                    fournisseurs.append(f)
            except Exception as e:
                print(f" Erreur lors de la récupération des fournisseurs : {e}")
            finally:
                cursor.close()
        return fournisseurs

    def get_by_id_or_code(self, identifiant):
        """Afficher les détails d'un fournisseur (par ID ou code)."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                if str(identifiant).isdigit():
                    query = "SELECT * FROM fournisseur WHERE id = %s"
                else:
                    query = "SELECT * FROM fournisseur WHERE code = %s"

                cursor.execute(query, (identifiant,))
                row = cursor.fetchone()
                if row:
                    return Fournisseur(id=row[0], code=row[1], raison_sociale=row[2],
                                       email=row[3], telephone=row[4], adresse=row[5], date_creation=row[6])
                else:
                    print("  Fournisseur introuvable.")
            except Exception as e:
                print(f" Erreur : {e}")
            finally:
                cursor.close()
        return None

    def update(self, fournisseur_id, nouvelle_raison, nouvel_email, nouveau_tel, nouvelle_adresse):
        """Modifier les informations d'un fournisseur."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = """
                    UPDATE fournisseur 
                    SET raison_sociale = %s, email = %s, telephone = %s, adresse = %s 
                    WHERE id = %s
                """
                values = (nouvelle_raison, nouvel_email, nouveau_tel, nouvelle_adresse, fournisseur_id)
                cursor.execute(query, values)
                self.conn.commit()

                if cursor.rowcount > 0:
                    print("✅ Fournisseur mis à jour avec succès !")
                else:
                    print("  Aucun fournisseur n'a été modifié (ID introuvable).")
            except Exception as e:
                self.conn.rollback()
                print(f" Erreur lors de la mise à jour : {e}")
            finally:
                cursor.close()

    def delete(self, fournisseur_id):
        """Supprimer un fournisseur (uniquement s'il n'a aucune commande associée)."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM fournisseur WHERE id = %s", (fournisseur_id,))
                self.conn.commit()
                print(" Fournisseur supprimé avec succès !")
            except Exception as e:
                self.conn.rollback()
                print(
                    f" Impossible de supprimer le fournisseur. Il a probablement des commandes associées. (Erreur technique: {e})")
            finally:
                cursor.close()

    def search_by_code_or_raison_sociale(self, mot_cle):
        """Rechercher un fournisseur par code ou par raison sociale."""
        fournisseurs_trouves = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                query = "SELECT * FROM fournisseur WHERE code LIKE %s OR raison_sociale LIKE %s"
                valeur_recherche = f"%{mot_cle}%"
                cursor.execute(query, (valeur_recherche, valeur_recherche))
                rows = cursor.fetchall()
                for row in rows:
                    f = Fournisseur(id=row[0], code=row[1], raison_sociale=row[2],
                                    email=row[3], telephone=row[4], adresse=row[5], date_creation=row[6])
                    fournisseurs_trouves.append(f)
            except Exception as e:
                print(f" Erreur de recherche : {e}")
            finally:
                cursor.close()
        return fournisseurs_trouves