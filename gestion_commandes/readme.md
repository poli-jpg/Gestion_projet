Gestion Commandes
Application Python en ligne de commande permettant de gérer des commandes, des produits et des fournisseurs, avec persistance des données en base de données.
Fonctionnalités
Gestion des commandes 
— création,consultation et suivi des commandes
— Gestion des produits 
— ajout et consultation du catalogue produits
— Gestion des fournisseurs 
— suivi des fournisseurs associés aux produits
Menu interactif 
— interface en ligne de commande pour naviguer entre les différentes fonctionnalités
Couche DAO (Data Access Object) 
— séparation claire entre la logique métier et l'accès aux données
Initialisation automatique de la base de données 
— création des tables 

Structure du projet
gestion_commandes/
├── models/              # Modèles métier (Commande, Produit, Fournisseur)
├── dao/
│   ├── produit_dao.py       # Accès aux données des produits
│   ├── fournisseur_dao.py   # Accès aux données des fournisseurs
│   └── commande_dao.py      # Accès aux données des commandes
├── menu/
│   └── interface.py     # Menu interactif de l'application
├── create_tables.py     # Script de création des tables en base
├── insert_test_data.py  # Script d'insertion de données de test
└── main.py               # Point d'entrée de l'application
Prérequis
Python 3.10 ou supérieur
Un système de gestion de base de données compatible (voir `requirements.txt`)
Installation
 Cloner le dépôt :
   bash
git clone https://github.com/poli-jpg/Commande_gestion.git
cd Commande_gestion

 Créer et activer un environnement virtuel (recommandé) :
   bash
python -m venv env
env\Scripts\activate      # Windows

Installer les dépendances :
   bash
pip install -r requirements.txt

Utilisation
 Créer les tables en base de données :
   bash
python gestion_commandes/create_tables.py

Technologies utilisées
Python
Architecture en couches (Models / DAO / Interface)
Membre du Groupe
Pape Latyr Séne
Mouhamed Konté
Amadou Sy
