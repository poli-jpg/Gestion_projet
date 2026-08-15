from datetime import datetime

from gestion_commandes.dao.fournisseur_dao import FournisseurDAO
from gestion_commandes.dao.produit_dao import ProduitDAO
from gestion_commandes.dao.commande_dao import CommandeDAO
from gestion_commandes.models.fournisseur import Fournisseur
from gestion_commandes.models.produit import Produit
from gestion_commandes.models.commande import Commande, LigneCommande


class Interface:
    def __init__(self):
        self.fournisseur_dao = FournisseurDAO()
        self.produit_dao = ProduitDAO()
        self.commande_dao = CommandeDAO()

    def menu_principal(self):
        while True:
            print("\n=======  MENU PRINCIPAL - GESTION DES COMMANDES FOURNISSEURS  =========")
            print("1. Gestion des fournisseurs")
            print("2. Gestion des produits")
            print("3. Gestion des commandes")
            print("4. Rapports et statistiques")
            print("5. Quitter")
            print("=========================================================================")
            try:
                choix = int(input("Faites votre choix : "))
            except ValueError:
                print("--- Veuillez saisir un nombre valide ---")
                continue

            match choix:
                case 1:
                    self.menu_fournisseurs()
                case 2:
                    self.menu_produits()
                case 3:
                    self.menu_commandes()
                case 4:
                    self.menu_rapports()
                case 5:
                    print("Au revoir et merci !!! ....")
                    break
                case _:
                    print("--- Choix invalide ---")

    # ------------------------------------------------------------------
    #               GESTION DES FOURNISSEURS
    # ------------------------------------------------------------------
    def menu_fournisseurs(self):
        while True:
            print("\n-------  GESTION DES FOURNISSEURS  -------")
            print("1. Ajouter un fournisseur")
            print("2. Lister les fournisseurs")
            print("3. Afficher un fournisseur par ID")
            print("4. Modifier un fournisseur")
            print("5. Supprimer un fournisseur")
            print("6. Rechercher un fournisseur par code ou raison social")
            print("7. Retour au menu principal")
            print("-------------------------------------------")
            choix = int(input("Faites votre choix : "))
            match choix:
                case 1:
                    def ajouter_fournisseur():
                        code = input("Code  : ")
                        raison_sociale = input("Raison sociale : ")
                        email = input("Email : ")
                        telephone = input("Telephone : ")
                        adresse = input("Adresse : ")
                        fournisseur = Fournisseur(code=code, raison_sociale=raison_sociale,
                                                  email=email, telephone=telephone, adresse=adresse)
                        if self.fournisseur_dao.create(fournisseur):
                            print("--- Fournisseur ajoute avec succes ---")
                        else:
                            print("--- Echec de l'ajout du fournisseur ---")

                    ajouter_fournisseur()

                case 2:
                    def lister_fournisseurs():
                        fournisseurs = self.fournisseur_dao.get_all()
                        if not fournisseurs:
                            print("--- Aucun fournisseur enregistre ---")
                        else:
                            for f in fournisseurs:
                                print(f)

                    lister_fournisseurs()

                case 3:
                    def afficher_fournisseur():
                        id_fournisseur = int(input("ID du fournisseur : "))
                        fournisseur = self.fournisseur_dao.get_by_id_or_code(id_fournisseur)
                        if fournisseur:
                            fournisseur.afficher()
                        else:
                            print("--- Fournisseur introuvable ---")

                    afficher_fournisseur()

                case 4:
                    def modifier_fournisseur():
                        id_fournisseur = int(input("ID du fournisseur a modifier : "))
                        fournisseur = self.fournisseur_dao.get_by_id_or_code(id_fournisseur)
                        if not fournisseur:
                            print("--- Fournisseur introuvable ---")
                            return
                        print("Laissez vide")
                        raison_sociale = input(
                            f"Raison sociale [{fournisseur.raison_sociale}] : ") or fournisseur.raison_sociale
                        email = input(f"Email [{fournisseur.email}] : ") or fournisseur.email
                        telephone = input(f"Telephone [{fournisseur.telephone}] : ") or fournisseur.telephone
                        adresse = input(f"Adresse [{fournisseur.adresse}] : ") or fournisseur.adresse
                        self.fournisseur_dao.update(id_fournisseur, raison_sociale, email, telephone, adresse)
                        print("--- Fournisseur modifie avec succes ---")

                    modifier_fournisseur()

                case 5:
                    def supprimer_fournisseur():
                        id_fournisseur = int(input("ID du fournisseur a supprimer : "))
                        self.fournisseur_dao.delete(id_fournisseur)

                    supprimer_fournisseur()

                case 6:
                    def rechercher_fournisseur():
                        mot_cle = input("Mot-cle : ")
                        resultats = self.fournisseur_dao.search_by_code_or_raison_sociale(mot_cle)
                        if resultats:
                            for f in resultats:
                                print(f)
                        else:
                            print("--- Aucun fournisseur trouve ---")

                    rechercher_fournisseur()

                case 7:
                    break
                case _:
                    print("--- Choix invalide ---")

    # ------------------------------------------------------------------
    #                   GESTION DES PRODUITS
    # ------------------------------------------------------------------
    def menu_produits(self):
        while True:
            print("\n-------  GESTION DES PRODUITS  -------")
            print("1. Ajouter un produit")
            print("2. Lister les produits")
            print("3. Afficher un produit (par ID)")
            print("4. Modifier un produit")
            print("5. Supprimer un produit")
            print("6. Rechercher un produit par designation")
            print("7. Alerte reapprovisionnement")
            print("8. Retour au menu principal")
            print("---------------------------------------")
            choix = int(input("Faites votre choix : "))
            match choix:
                case 1:
                    def ajouter_produit():
                        id_saisi = input("ID () : ").strip()
                        id_produit = int(id_saisi) if id_saisi else None

                        reference = input("Reference () : ")
                        designation = input("Designation : ")
                        prix_unitaire = float(input("Prix unitaire : "))
                        stock = int(input("Stock initial : "))

                        date_saisie = input(
                            "Date d'ajout : ").strip()
                        if date_saisie:
                            try:
                                date_creation = datetime.strptime(date_saisie, "%Y-%m-%d").date()
                            except ValueError:
                                print("--- Format de date invalide, date du jour utilisee ---")
                                date_creation = None
                        else:
                            date_creation = None

                        produit = Produit(reference=reference, designation=designation,
                                          prix_unitaire=prix_unitaire, stock=stock,
                                          id=id_produit, date_creation=date_creation)
                        if self.produit_dao.create(produit):
                            print("--- Produit ajoute avec succes ---")
                        else:
                            print("--- Echec de l'ajout du produit ---")

                    ajouter_produit()

                case 2:
                    def lister_produits():
                        produits = self.produit_dao.get_all()
                        if not produits:
                            print("--- Aucun produit enregistre ---")
                        else:
                            for p in produits:
                                print(p)

                    lister_produits()

                case 3:
                    def afficher_produit():
                        id_produit = int(input("ID du produit : "))
                        produit = self.produit_dao.get_by_id_or_ref(id_produit)
                        if produit:
                            produit.afficher()
                        else:
                            print("--- Produit introuvable ---")

                    afficher_produit()

                case 4:
                    def modifier_produit():
                        id_produit = int(input("ID du produit a modifier : "))
                        produit = self.produit_dao.get_by_id_or_ref(id_produit)
                        if not produit:
                            print("--- Produit introuvable ---")
                            return
                        print("Laissez vide pour ne pas modifier un champ")
                        designation = input(f"Designation [{produit.designation}] : ") or produit.designation
                        prix_saisi = input(f"Prix unitaire [{produit.prix_unitaire}] : ")
                        stock_saisi = input(f"Stock [{produit.stock}] : ")
                        prix = float(prix_saisi) if prix_saisi else produit.prix_unitaire
                        stock = int(stock_saisi) if stock_saisi else produit.stock
                        if self.produit_dao.update(id_produit, designation, prix, stock):
                            print("--- Produit modifie avec succes ---")
                        else:
                            print("--- Echec de la modification ---")

                    modifier_produit()

                case 5:
                    def supprimer_produit():
                        id_produit = int(input("ID du produit a supprimer : "))
                        if self.produit_dao.delete(id_produit):
                            print("--- Produit supprime avec succes ---")
                        else:
                            print("--- Echec ---")

                    supprimer_produit()

                case 6:
                    def rechercher_produit():
                        mot_cle = input("Designation : ")
                        resultats = self.produit_dao.search_by_designation(mot_cle)
                        if resultats:
                            for p in resultats:
                                print(p)
                        else:
                            print("--- Aucun produit trouve ---")

                    rechercher_produit()

                case 7:
                    def alerte_reapprovisionnement():
                        seuil = int(input("Seuil  : "))
                        produits = self.produit_dao.get_alertes_stock(seuil)
                        if produits:
                            print(f"--- Produits sous le seuil de {seuil} ---")
                            for p in produits:
                                print(p)
                        else:
                            print("--- Aucun produit sous ce seuil ---")

                    alerte_reapprovisionnement()

                case 8:
                    break
                case _:
                    print("--- Choix invalide ---")

    # ------------------------------------------------------------------
    #                   GESTION DES COMMANDES
    # ------------------------------------------------------------------
    def menu_commandes(self):
        while True:
            print("\n-------  GESTION DES COMMANDES  -------")
            print("1. Creer une commande")
            print("2. Lister les commandes")
            print("3. Afficher le detail d'une commande")
            print("4. Changer le statut d'une commande")
            print("5. Annuler une commande")
            print("6. Supprimer une commande")
            print("7. Retour au menu principal")
            print("-----------------------------------------")
            choix = int(input("Faites votre choix : "))
            match choix:
                case 1:
                    def creer_commande():
                        numero = input("Numero de commande ) : ")
                        try:
                            id_fournisseur = int(input("ID du fournisseur : "))
                        except ValueError:
                            print("--- Veuillez saisir un nombre valide ---")
                            return

                        fournisseur = self.fournisseur_dao.get_by_id_or_code(id_fournisseur)
                        if not fournisseur:
                            print("--- Fournisseur introuvable ---")
                            return

                        produits_dispo = self.produit_dao.get_all()
                        if not produits_dispo:
                            print("--- Aucun produit enregistre, impossible de creer une commande ---")
                            return

                        print("\n--- Produits disponibles ---")
                        for p in produits_dispo:
                            print(p)
                        print("-----------------------------")

                        lignes = []
                        recap = []
                        while True:
                            try:
                                id_produit = int(input("ID du produit ) : "))
                            except ValueError:
                                print("--- Veuillez saisir un nombre valide ---")
                                continue

                            if id_produit == 0:
                                break
                            produit = self.produit_dao.get_by_id_or_ref(id_produit)
                            if not produit:
                                print("--- Produit introuvable ---")
                                continue

                            try:
                                quantite = int(input(f"Quantite (stock disponible : {produit.stock}) : "))
                            except ValueError:
                                print("--- Veuillez saisir un nombre valide ---")
                                continue

                            lignes.append(LigneCommande(produit_id=id_produit, quantite=quantite,
                                                        prix_unitaire=produit.prix_unitaire))
                            recap.append((produit.designation, quantite, produit.prix_unitaire))

                            print("\n--- Produits deja ajoutes a cette commande ---")
                            for designation, qte, pu in recap:
                                print(f"{designation} - Qte : {qte} - PU : {pu} - "
                                      f"Sous-total : {qte * pu}")
                            print("-----------------------------------------------\n")

                        if not lignes:
                            print("--- Aucun produit ajoute, commande annulee ---")
                            return

                        commande = Commande(numero=numero, fournisseur_id=id_fournisseur)
                        commande.lignes = lignes
                        if self.commande_dao.create(commande):
                            print("--- Commande creee avec succes ---")
                        else:
                            print("--- Echec de la creation de la commande ---")

                    creer_commande()

                case 2:
                    def lister_commandes():
                        commandes = self.commande_dao.get_all()
                        if not commandes:
                            print("--- Aucune commande enregistree ---")
                        else:
                            for c in commandes:
                                print(c)

                    lister_commandes()

                case 3:
                    def afficher_detail_commande():
                        try:
                            id_commande = int(input("ID de la commande : "))
                        except ValueError:
                            print("--- Veuillez saisir un nombre valide ---")
                            return
                        commande = self.commande_dao.get_by_id(id_commande)
                        if not commande:
                            print("--- Commande introuvable ---")
                            return
                        commande.afficher()
                        print("--- Lignes de la commande ---")
                        print("(Détail des lignes non disponible actuellement)")

                    afficher_detail_commande()

                case 4:
                    def changer_statut_commande():
                        try:
                            id_commande = int(input("ID de la commande : "))
                        except ValueError:
                            print("--- Veuillez saisir une commande valide ---")
                            return
                        print("Statuts possibles : EN_ATTENTE, VALIDEE, LIVREE")
                        nouveau_statut = input("Nouveau statut : ").strip().upper()
                        self.commande_dao.changer_statut(id_commande, nouveau_statut)
                        print("--- Statut mis a jour ---")

                    changer_statut_commande()

                case 5:
                    def annuler_commande():
                        try:
                            id_commande = int(input("ID de la commande a annuler : "))
                        except ValueError:
                            print("--- Veuillez saisir une commande valide ---")
                            return
                        self.commande_dao.delete(id_commande)
                        print("--- Commande annulee ---")

                    annuler_commande()

                case 6:
                    def supprimer_commande():
                        id_commande = int(input("ID de la commande a supprimer : "))
                        self.commande_dao.delete(id_commande)
                        print("--- Commande supprimee avec succes ---")

                    supprimer_commande()

                case 7:
                    break
                case _:
                    print("--- Choix invalide ---")

    # ------------------------------------------------------------------
    #                   RAPPORTS ET STATISTIQUES
    # ------------------------------------------------------------------
    def menu_rapports(self):
        while True:
            print("\n-------  RAPPORTS ET STATISTIQUES  -------")
            print("1. Commandes par fournisseur")
            print("2. Commandes en attente de validation")
            print("3. Valeur totale du stock")
            print("4. Top 5 des produits les plus commandes")
            print("5. Chiffre d'affaires total")
            print("6. Retour au menu principal")
            print("--------------------------------------------")
            choix = int(input("Faites votre choix : "))
            match choix:
                case 1:
                    def commandes_par_fournisseur():
                        id_fournisseur = int(input("ID du fournisseur : "))
                        commandes = self.commande_dao.get_all()
                        resultats = [c for c in commandes if c.fournisseur_id == id_fournisseur]
                        if resultats:
                            for c in resultats:
                                print(c)
                        else:
                            print("--- Aucune commande pour ce fournisseur ---")

                    commandes_par_fournisseur()

                case 2:
                    def commandes_en_attente():
                        commandes = self.commande_dao.get_all()
                        resultats = [c for c in commandes if c.statut == "EN_ATTENTE"]
                        if resultats:
                            for c in resultats:
                                print(c)
                        else:
                            print("--- Aucune commande en attente ---")

                    commandes_en_attente()

                case 3:
                    def valeur_totale_stock():
                        produits = self.produit_dao.get_all()
                        valeur = sum(p.prix_unitaire * p.stock for p in produits)
                        print(f"--- Valeur totale du stock : {valeur} FCFA ---")

                    valeur_totale_stock()

                case 4:
                    def top_5_produits():
                        print("--- Fonctionnalite non disponible ---")

                    top_5_produits()

                case 5:
                    def chiffre_affaires_total():
                        commandes = self.commande_dao.get_all()
                        total = sum(c.montant_total for c in commandes if c.statut in ["VALIDEE", "LIVREE"])
                        print(f"--- Chiffre d'affaires total : {total} FCFA ---")

                    chiffre_affaires_total()

                case 6:
                    break
                case _:
                    print("--- Choix invalide ---")