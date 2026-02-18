import json
from datetime import datetime

# ==========================================
# 1. EXCEPTIONS PERSONNALISÉES
# ==========================================
class SoldeInsuffisantError(Exception):
    pass

class PlafondDepasserError(Exception):
    pass

# ==========================================
# 2. CLASSES PRINCIPALES
# ==========================================
class Compte:
    def __init__(self, titulaire, solde_initial=0):
        self.titulaire = titulaire
        self.solde = solde_initial
        self.historique = []
        self._ajouter_historique("Ouverture", solde_initial)

    def _ajouter_historique(self, type_op, montant):
        entry = {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "operation": type_op,
            "montant": montant,
            "solde_final": self.solde
        }
        self.historique.append(entry)

    def deposer(self, montant):
        if montant > 0:
            self.solde += montant
            self._ajouter_historique("Dépôt", montant)
            print(f"✅ Dépôt réussi. Nouveau solde : {self.solde}€")
        return self.solde

    def retirer(self, montant):
        if montant > self.solde:
            raise SoldeInsuffisantError(f"Solde insuffisant ({self.solde}€).")
        self.solde -= montant
        self._ajouter_historique("Retrait", montant)
        print(f"✅ Retrait réussi. Nouveau solde : {self.solde}€")
        return self.solde

    def to_dict(self):
        return {"titulaire": self.titulaire, "solde": self.solde, "type": self.__class__.__name__, "historique": self.historique}

class ComptePro(Compte):
    def __init__(self, titulaire, solde_initial=0, plafond=1000):
        super().__init__(titulaire, solde_initial)
        self.plafond = plafond

    def retirer(self, montant):
        if montant > self.plafond:
            raise PlafondDepasserError(f"Limite de {self.plafond}€ dépassée.")
        return super().retirer(montant)

# ==========================================
# 3. INTERFACE UTILISATEUR (MENU)
# ==========================================
def menu_principal():
    print("\n--- BIENVENUE À LA BANQUE PYTHON ---")
    nom = input("Entrez votre nom : ")
    print("Choisissez votre type de compte :")
    print("1. Compte Standard")
    print("2. Compte Pro (Plafond 1000€)")
    
    choix_type = input("Votre choix (1 ou 2) : ")
    if choix_type == "2":
        mon_compte = ComptePro(nom, solde_initial=100)
    else:
        mon_compte = Compte(nom, solde_initial=100)

    while True:
        print(f"\n--- MENU DE {mon_compte.titulaire.upper()} ---")
        print(f"Solde actuel : {mon_compte.solde}€")
        print("1. Faire un versement (Dépôt)")
        print("2. Faire un retrait")
        print("3. Voir l'historique")
        print("4. Sauvegarder et Quitter")
        
        choix = input("\nQue voulez-vous faire ? : ")

        try:
            if choix == "1":
                mtt = float(input("Montant à déposer : "))
                mon_compte.deposer(mtt)
            
            elif choix == "2":
                mtt = float(input("Montant à retirer : "))
                mon_compte.retirer(mtt)
            
            elif choix == "3":
                print("\n--- HISTORIQUE DES TRANSACTIONS ---")
                for h in mon_compte.historique:
                    print(f"{h['date']} | {h['operation']} : {h['montant']}€ | Solde : {h['solde_final']}€")
            
            elif choix == "4":
                # Sauvegarde en JSON avant de partir
                with open("banque.json", "w", encoding="utf-8") as f:
                    json.dump(mon_compte.to_dict(), f, indent=4)
                print("Données enregistrées. Au revoir !")
                break
            
            else:
                print("⚠️ Choix invalide.")

        except (SoldeInsuffisantError, PlafondDepasserError) as e:
            print(f"❌ ERREUR : {e}")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    menu_principal()