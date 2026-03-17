import projet_info

projet_info.createAllTables()

#vider les tables avant test
projet_info.delete_Consommation("")
projet_info.delete_Planification("")
projet_info.delete_Process("")
projet_info.delete_Commande("")
projet_info.delete_Machine("")
projet_info.delete_Electricite("")
projet_info.delete_Produit("")
projet_info.delete_Operateur("")

projet_info.insert_Operateur("Anis","Anis@gmail.com")
projet_info.insert_Operateur("Walid","Walid@gmail.com")

projet_info.insert_Machine("Four",20,2000,2)
projet_info.insert_Machine("Mixeur", 10,500,1)
projet_info.insert_Machine("Micro_onde",15,1500,1)
projet_info.insert_Machine("Cuiseur",30,1000,2)

projet_info.insert_Produit("Soupe")
projet_info.insert_Produit("Biscuit")
projet_info.insert_Produit("Pain")
projet_info.insert_Produit("Sauce")

# Soupe (produit 1)
projet_info.insert_Process(4, 1, 1)
projet_info.insert_Process(1, 1, 2)

# Biscuit (produit 2)
projet_info.insert_Process(1, 2, 1)
projet_info.insert_Process(2, 2, 2)
projet_info.insert_Process(3, 2, 3)

# Pain (produit 3)
projet_info.insert_Process(1, 3, 1)
projet_info.insert_Process(2, 3, 2)

# Sauce (produit 4)
projet_info.insert_Process(4, 4, 1)
projet_info.insert_Process(1, 4, 2)

# Ajouter des commandes
projet_info.insert_Commande(120.5, "2026-03-15")  # Commande 1
projet_info.insert_Commande(85.0, "2026-03-15")   # Commande 2

# Planification des produits pour chaque commande

# Planifier la production de "Soupe" pour la commande 1 à 08:00
projet_info.insert_Planification(1, 1, "2026-03-15 08:00:00")

# Planifier la production de "Biscuit" pour la commande 2 à 09:00
projet_info.insert_Planification(2, 2, "2026-03-15 09:00:00")

# Vérification des données
print(projet_info.select_Operateur(""))
print(projet_info.select_Machine(""))
print(projet_info.select_Produit(""))
print(projet_info.select_Commande(""))
print(projet_info.select_Planification(""))

