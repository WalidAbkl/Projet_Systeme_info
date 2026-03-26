
import pandas as pd
from entsoe import EntsoePandasClient
import usine  # Utilise ton fichier usine.py pour l'insertion SQL

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

        # 4. PARCOURS DES DONNÉES ET INSERTION DANS TA BASE
        for timestamp, price in ts.items():
            # Conversion pour ton format SQL dans usine.py
            date_sql = timestamp.strftime('%Y-%m-%d')
            heure_sql = timestamp.hour
            
            # Appel de ta fonction : insert_Electricite(date, heure, prix, quart_d_heure)
            # On met 0 pour quart_d_heure car l'API donne des prix à l'heure
            usine.insert_Electricite(date_sql, heure_sql, round(price, 2), 0)
            
            # Affichage console pour vérification
            print(f"Ajouté : {heure_sql}h -> {price} €/MWh")

            # ALERTE PRIX NÉGATIF (Point 6 du cahier des charges)
            if price < 0:
                print(f"⚠️ ALERTE : Prix négatif détecté à {heure_sql}h !")

        print("\n✅ Importation terminée avec succès dans usine.db")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("Vérifie ta connexion internet ou si ton Token est bien activé par ENTSO-E.")

if __name__ == "__main__":
    # On crée les tables si elles n'existent pas encore
    usine.createAllTables()
    # On lance l'importation
    importer_prix_du_jour()






