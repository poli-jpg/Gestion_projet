
from gestion_commandes.dao.base_dao import BaseDAO
from gestion_commandes.models.commande import Commande, LigneCommande


class CommandeDAO(BaseDAO):

    def create(self, commande):
        """
        Crée une commande et ses lignes de détails.
        Utilise une transaction pour garantir que tout est ajouté ou rien du tout.
        """
        try:
            cursor = self.conn.cursor()
            query_cmd = """INSERT INTO commande (numero, fournisseur_id, montant_total, statut) 
                           VALUES (%s, %s, %s, %s)"""
            cursor.execute(query_cmd, (commande.numero, commande.fournisseur_id,
                                       commande.montant_total, commande.statut))

            commande_id = cursor.lastrowid

            for ligne in commande.lignes:
                query_ligne = """INSERT INTO ligne_commande (commande_id, produit_id, quantite, prix_unitaire) 
                                 VALUES (%s, %s, %s, %s)"""
                cursor.execute(query_ligne, (commande_id, ligne.produit_id, ligne.quantite, ligne.prix_unitaire))

                query_stock = "UPDATE produit SET stock = stock - %s WHERE id = %s"
                cursor.execute(query_stock, (ligne.quantite, ligne.produit_id))

            self.conn.commit()
            print(" Commande enregistrée et stocks mis à jour avec succès !")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f" Erreur lors de la création de la commande : {e}")
            return False
        finally:
            cursor.close()

    def get_all(self):
        commandes = []
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    "SELECT id, numero, fournisseur_id, montant_total, statut, date_commande, date_creation FROM commande")
                rows = cursor.fetchall()
                for row in rows:
                    commandes.append(Commande(id=row[0], numero=row[1], fournisseur_id=row[2],
                                              montant_total=row[3], statut=row[4], date_commande=row[5],
                                              date_creation=row[6]))
            except Exception as e:
                print(f" Erreur lors de la récupération des commandes : {e}")
            finally:
                cursor.close()
        return commandes

    def get_by_id(self, identifiant):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    "SELECT id, numero, fournisseur_id, montant_total, statut, date_commande, date_creation FROM commande WHERE id = %s",
                    (identifiant,))
                row = cursor.fetchone()
                if row:
                    return Commande(id=row[0], numero=row[1], fournisseur_id=row[2],
                                    montant_total=row[3], statut=row[4], date_commande=row[5],
                                    date_creation=row[6])
            except Exception as e:
                print(f" Erreur lors de la récupération de la commande : {e}")
            finally:
                cursor.close()
        return None

    def delete(self, identifiant):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM ligne_commande WHERE commande_id = %s", (identifiant,))
                cursor.execute("DELETE FROM commande WHERE id = %s", (identifiant,))
                self.conn.commit()
                print("Commande supprimée avec succès !")
            except Exception as e:
                self.conn.rollback()
                print(f" Erreur lors de la suppression de la commande : {e}")
            finally:
                cursor.close()

    def changer_statut(self, commande_id, nouveau_statut):
        """Permet de changer le statut (ex: EN_ATTENTE -> LIVREE)."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE commande SET statut = %s WHERE id = %s", (nouveau_statut, commande_id))
            self.conn.commit()
            print(" Statut mis à jour.")
        except Exception as e:
            self.conn.rollback()
            print(f" Erreur : {e}")
        finally:
            cursor.close()