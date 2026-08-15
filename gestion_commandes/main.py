from gestion_commandes.menu.interface import Interface

def main():
    print("Bienvenue dans l'application de gestion des commandes !")
    print("=" * 50)
    print("\n")
    interface = Interface()
    interface.menu_principal()

if __name__ == "__main__":
    main()