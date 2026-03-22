import usine

usine.createAllTables()

# Vider les tables avant test (ordre important à cause des clés étrangères)
usine.delete_Consommation("")
usine.delete_Planification("")
usine.delete_Process("")
usine.delete_Commande("")
usine.delete_Machine("")
usine.delete_Electricite("")
usine.delete_Produit("")
usine.delete_Operateur("")

# OPÉRATEURS
usine.insert_Operateur("Walid", "23186@ecam.be")
usine.insert_Operateur("Anis", "23076@ecam.be")

# Récupérer les vrais IDs générés
operateurs = usine.select_Operateur("")
id_walid = operateurs[0][0]
id_anis = operateurs[1][0]

# MACHINES
usine.insert_Machine("Fraiseuse CNC", 45, 15000, id_walid)
usine.insert_Machine("Tour",          30,  8000, id_walid)
usine.insert_Machine("Soudure",       20,  5000, id_anis)
usine.insert_Machine("Ponceuse",      15,  1500, id_anis)

# Récupérer les vrais IDs des machines
machines = usine.select_Machine("")
id_fraiseuse = machines[0][0]
id_tour      = machines[1][0]
id_soudure   = machines[2][0]
id_ponceuse  = machines[3][0]

# PRODUITS
usine.insert_Produit("Engrenage")
usine.insert_Produit("Arbre de transmission")
usine.insert_Produit("Chassis soude")
usine.insert_Produit("Piston")

# Récupérer les vrais IDs des produits
produits = usine.select_Produit("")
id_engrenage = produits[0][0]
id_arbre     = produits[1][0]
id_chassis   = produits[2][0]
id_piston    = produits[3][0]

# PROCESS
# Engrenage : Tour → Fraiseuse CNC → Ponceuse
usine.insert_Process(id_tour,      id_engrenage, 1)
usine.insert_Process(id_fraiseuse, id_engrenage, 2)
usine.insert_Process(id_ponceuse,  id_engrenage, 3)

# Arbre de transmission : Tour → Fraiseuse CNC → Ponceuse
usine.insert_Process(id_tour,      id_arbre, 1)
usine.insert_Process(id_fraiseuse, id_arbre, 2)
usine.insert_Process(id_ponceuse,  id_arbre, 3)

# Chassis soude : Fraiseuse CNC → Soudure → Ponceuse
usine.insert_Process(id_fraiseuse, id_chassis, 1)
usine.insert_Process(id_soudure,   id_chassis, 2)
usine.insert_Process(id_ponceuse,  id_chassis, 3)

# Piston : Tour → Fraiseuse CNC → Ponceuse
usine.insert_Process(id_tour,      id_piston, 1)
usine.insert_Process(id_fraiseuse, id_piston, 2)
usine.insert_Process(id_ponceuse,  id_piston, 3)

# VÉRIFICATION
print("=== Opérateurs ===")
print(usine.select_Operateur(""))
print("\n=== Machines ===")
print(usine.select_Machine(""))
print("\n=== Produits ===")
print(usine.select_Produit(""))
print("\n=== Process ===")
print(usine.select_Process(""))