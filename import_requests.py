# import requests

# # URL de la requête API avec le nouveau token
# url = "https://web-api.tp.entsoe.eu/api?securityToken=e409b908-a869-4320-8ad6-b16c27a9c4c8&documentType=A68&processType=A33&in_Domain=10YBE----------2&periodStart=202602100000&periodEnd=202602102300"

# # Faire la requête HTTP
# response = requests.get(url)

# # Vérifier que la requête a réussi
# if response.status_code == 200:
#     print("Données récupérées avec succès")
#     print(response.text)  # Afficher les données retournées (format XML)
# else:
#     print("Erreur lors de la récupération des données", response.status_code)

import pandas as pd
from entsoe import EntsoePandasClient
import matplotlib.pyplot as plt  # <-- NOUVEL IMPORT POUR LE GRAPHIQUE
import io                        # <-- NOUVEL IMPORT POUR SAUVEGARDER L'IMAGE EN MÉMOIRE
import usine  # Utilise ton fichier usine.py pour l'insertion SQL
import mail   # Importation de ton module mail pour envoyer les alertes

# 1. TON TOKEN DÉJÀ INTÉGRÉ
TOKEN = "e409b908-a869-4320-8ad6-b16c27a9c4c8"
client = EntsoePandasClient(api_key=TOKEN)

# 2. DATES AUTOMATIQUES (Aujourd'hui)
# On définit le début et la fin de la journée actuelle
start = pd.Timestamp.now(tz='Europe/Brussels').floor('D')
end = start + pd.Timedelta(days=1)

def importer_prix_du_jour():
    try:
        print(f"--- Connexion à ENTSO-E pour la date du {start.date()} ---")
        
        # 3. RÉCUPÉRATION DES PRIX BELGIQUE
        # query_day_ahead_prices renvoie une Série Pandas avec (Temps, Prix)
        ts = client.query_day_ahead_prices('BE', start=start, end=end)

        # Récupération de la liste de tous les opérateurs dans la base de données
        liste_operateurs = usine.select_Operateur("")

        presence_prix_negatif = False

        # 4. PARCOURS DES DONNÉES ET INSERTION DANS TA BASE
        for timestamp, price in ts.items():
            # Conversion pour ton format SQL dans usine.py
            date_sql = timestamp.strftime('%Y-%m-%d')
            heure_sql = timestamp.hour
            prix_arrondi = round(price, 2)
            
            # Appel de ta fonction : insert_Electricite(date, heure, prix, quart_d_heure)
            # On met 0 pour quart_d_heure car l'API donne des prix à l'heure
            usine.insert_Electricite(date_sql, heure_sql, prix_arrondi, 0)
            
            # Affichage console pour vérification
            print(f"Ajouté : {heure_sql}h -> {prix_arrondi} €/MWh")

            # On vérifie si un prix négatif existe pour déclencher le graphique plus tard
            if price < 0:
                presence_prix_negatif = True

        # 5. GÉNÉRATION DU GRAPHIQUE ET ENVOI DES MAILS
        if presence_prix_negatif:
            print("\n⚠️ Prix négatifs détectés ! Génération du graphique et envoi des alertes...")
            
            # --- CRÉATION DU GRAPHIQUE ---
            plt.figure(figsize=(10, 5))
            
            # Les heures sur l'axe X, et les prix sur l'axe Y
            heures = ts.index.hour
            prix = ts.values
            
            # On met les barres en rouge si < 0, sinon en bleu
            couleurs = ['red' if p < 0 else '#4C72B0' for p in prix]
            
            plt.bar(heures, prix, color=couleurs)
            plt.axhline(0, color='black', linewidth=1) # Ligne du Zéro
            plt.xlabel('Heure de la journée')
            plt.ylabel('Prix (€/MWh)')
            plt.title(f"Prix de l'électricité - Day Ahead (Belgique) - {start.date()}")
            plt.xticks(range(0, 24))
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # On sauvegarde le graphique dans un buffer (en mémoire vive)
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight')
            img_buf.seek(0)
            plt.close() # On ferme le plot pour libérer la mémoire
            
            # On récupère les octets de l'image
            image_bytes = img_buf.getvalue()

            # --- ENVOI DES MAILS ---
            for op in liste_operateurs:
                mail_destinataire = op[2] 
                mail.envoyer_alerte_prix_negatif(mail_destinataire, image_bytes)
                
        else:
            print("\nℹ️ Aucun prix négatif détecté pour aujourd'hui. Aucune alerte envoyée.")

        print("\n✅ Importation terminée avec succès.")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("Vérifie ta connexion internet ou si ton Token est bien activé par ENTSO-E.")

if __name__ == "__main__":
    # On crée les tables si elles n'existent pas encore
    usine.createAllTables()
    # On lance l'importation
    importer_prix_du_jour()