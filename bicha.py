import usine

# 1. RÉGÉNÉRATION
# Supprime manuellement usine.db avant de lancer ce script !
usine.createAllTables()

# Vider les tables
usine.delete_Process("")
usine.delete_Machine("")
usine.delete_Produit("")
usine.delete_Operateur("")

# 2. OPÉRATEURS
usine.insert_Operateur("Walid", "23186@ecam.be")
usine.insert_Operateur("Anis", "23076@ecam.be")

# 3. MACHINES (3 arguments : Nom, Puissance, ID_Operateur)
# Plus aucune durée ici ! [cite: 1, 6, 13]
usine.insert_Machine("Fraiseuse CNC", 15000, 1)
usine.insert_Machine("Tour", 8000, 1)

# 4. PRODUITS (1 seul argument : Nom)
# Le produit n'a plus de durée propre [cite: 1, 12]
usine.insert_Produit("Engrenage")
usine.insert_Produit("Piston")

# 5. PROCESS (4 arguments : id_machine, id_produit, sequence, DUREE)
# C'est ici que tu définis le temps spécifique 
# Engrenage sur Tour (Etape 1) pendant 30 min
usine.insert_Process(2, 1, 1, 30) 
# Piston sur Tour (Etape 1) pendant 40 min
usine.insert_Process(2, 2, 1, 40) 

print("✅ Base de données initialisée avec succès !")