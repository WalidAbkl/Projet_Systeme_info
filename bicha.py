import projet_info

projet_info.createAllTables()

#vider les tables avant test
# projet_info.delete_Consommation("")
# projet_info.delete_Planification("")
# projet_info.delete_Process("")
# projet_info.delete_Commande("")
# projet_info.delete_Machine("")
# projet_info.delete_Electricite("")
# projet_info.delete_Produit("")
# projet_info.delete_Operateur("")

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



