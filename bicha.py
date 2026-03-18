import usine

usine.createAllTables()

#vider les tables avant test
usine.delete_Consommation("")
usine.delete_Planification("")
usine.delete_Process("")
usine.delete_Commande("")
usine.delete_Machine("")
usine.delete_Electricite("")
usine.delete_Produit("")
usine.delete_Operateur("")

usine.insert_Operateur("Anis","Anis@gmail.com")
usine.insert_Operateur("Walid","Walid@gmail.com")

usine.insert_Machine("Four",20,2000,2)
usine.insert_Machine("Mixeur", 10,500,1)
usine.insert_Machine("Micro_onde",15,1500,1)
usine.insert_Machine("Cuiseur",30,1000,2)

usine.insert_Produit("Soupe")
usine.insert_Produit("Biscuit")
usine.insert_Produit("Pain")
usine.insert_Produit("Sauce")

# Soupe (produit 1)
usine.insert_Process(4, 1, 1)
usine.insert_Process(1, 1, 2)

# Biscuit (produit 2)
usine.insert_Process(1, 2, 1)
usine.insert_Process(2, 2, 2)
usine.insert_Process(3, 2, 3)

# Pain (produit 3)
usine.insert_Process(1, 3, 1)
usine.insert_Process(2, 3, 2)

# Sauce (produit 4)
usine.insert_Process(4, 4, 1)
usine.insert_Process(1, 4, 2)

# Ajouter des commandes
usine.insert_Commande(120.5, "2026-03-15")  # Commande 1
usine.insert_Commande(85.0, "2026-03-15")   # Commande 2

# Planification des produits pour chaque commande

# Planifier la production de "Soupe" pour la commande 1 à 08:00
usine.insert_Planification(1, 1, "2026-03-15 08:00:00")

# Planifier la production de "Biscuit" pour la commande 2 à 09:00
usine.insert_Planification(2, 2, "2026-03-15 09:00:00")

# Vérification des données
print(usine.select_Operateur(""))
print(usine.select_Machine(""))
print(usine.select_Produit(""))
print(usine.select_Commande(""))
print(usine.select_Planification(""))

