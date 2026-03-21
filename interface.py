from PyQt6 import QtWidgets, QtSql, uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQueryModel
import sys
import usine


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface_projet.ui", self)

        # --- Tab 1 : Configuration ---
        self.pushButton_add_operateur.clicked.connect(self.add_operateur)
        self.pushButton_add_machine.clicked.connect(self.add_machine)

        # --- Tab 2 : Produits & Process ---
        self.pushButton_add_produit.clicked.connect(self.add_produit)
        self.pushButton_add_process.clicked.connect(self.add_process)
        self.comboBox_produit.currentIndexChanged.connect(self.load_process_table)

        # --- Tab 3 : Commandes ---
        self.pushButton_calculer.clicked.connect(self.calculer_cout)
        self.pushButton_valider_commande.clicked.connect(self.valider_commande)

        self.setup_database()
        self.setup_models()
        self.load_tables()
        self.load_operateurs_combo()
        self.load_produits_combo()
        self.load_machines_combo()
        self.load_produits_commande_combo()
        self.setup_commandes_table()

    # -------------------------------------------------------
    # BASE DE DONNÉES
    # -------------------------------------------------------
    def setup_database(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("usine.db")

        if not self.db.open():
            QtWidgets.QMessageBox.critical(
                self, "Erreur base de données", self.db.lastError().text()
            )
            raise RuntimeError("Impossible d'ouvrir la base de données")

    def setup_models(self):
        # Modèle Table Machines (Tab 1)
        self.machines_model = QtSql.QSqlRelationalTableModel(self, self.db)
        self.machines_model.setTable("Machine")
        self.tableView_machines.setModel(self.machines_model)

        # Modèle Table Produits (Tab 2)
        self.produits_model = QtSql.QSqlRelationalTableModel(self, self.db)
        self.produits_model.setTable("Produit")
        self.tableView_produits.setModel(self.produits_model)

    def load_tables(self):
        if not self.machines_model.select():
            QtWidgets.QMessageBox.critical(
                self, "Erreur SQL", self.machines_model.lastError().text()
            )
        self.tableView_machines.setColumnHidden(0, True)
        self.tableView_machines.setColumnHidden(4, True)

        if not self.produits_model.select():
            QtWidgets.QMessageBox.critical(
                self, "Erreur SQL", self.produits_model.lastError().text()
            )
        self.tableView_produits.setColumnHidden(0, True)

    # -------------------------------------------------------
    # TAB 1 : OPÉRATEURS & MACHINES
    # -------------------------------------------------------
    def load_operateurs_combo(self):
        self.comboBox_operateur.clear()
        operateurs = usine.select_Operateur("")
        for op in operateurs:
            self.comboBox_operateur.addItem(op[1], op[0])

    def add_operateur(self):
        nom = self.lineEdit_nom.text().strip()
        mail = self.lineEdit_mail.text().strip()

        if not nom or not mail:
            QtWidgets.QMessageBox.warning(
                self, "Champs manquants", "Veuillez remplir le nom et l'email."
            )
            return

        usine.insert_Operateur(nom, mail)
        self.lineEdit_nom.clear()
        self.lineEdit_mail.clear()
        self.load_operateurs_combo()

    def add_machine(self):
        nom = self.lineEdit_nom_machine.text().strip()
        duree = self.lineEdit_duree.text().strip()
        puissance = self.lineEdit_puissance.text().strip()

        if not nom or not duree or not puissance:
            QtWidgets.QMessageBox.warning(
                self, "Champs manquants", "Veuillez remplir tous les champs de la machine."
            )
            return

        try:
            duree = int(duree)
            puissance = float(puissance)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Valeurs invalides", "Durée doit être un entier et puissance un nombre."
            )
            return

        id_op = self.comboBox_operateur.currentData()
        if id_op is None:
            QtWidgets.QMessageBox.warning(
                self, "Aucun opérateur", "Veuillez d'abord ajouter un opérateur."
            )
            return

        usine.insert_Machine(nom, duree, puissance, id_op)
        self.lineEdit_nom_machine.clear()
        self.lineEdit_duree.clear()
        self.lineEdit_puissance.clear()
        self.machines_model.select()
        self.tableView_machines.setColumnHidden(0, True)
        self.tableView_machines.setColumnHidden(4, True)
        self.load_machines_combo()

    # -------------------------------------------------------
    # TAB 2 : PRODUITS & PROCESS
    # -------------------------------------------------------
    def load_produits_combo(self):
        self.comboBox_produit.clear()
        produits = usine.select_Produit("")
        for p in produits:
            self.comboBox_produit.addItem(p[1], p[0])
        self.load_process_table()

    def load_machines_combo(self):
        self.comboBox_machine_process.clear()
        machines = usine.select_Machine("")
        for m in machines:
            self.comboBox_machine_process.addItem(m[1], m[0])

    def add_produit(self):
        nom = self.lineEdit_nom_produit.text().strip()

        if not nom:
            QtWidgets.QMessageBox.warning(
                self, "Champ manquant", "Veuillez entrer un nom de produit."
            )
            return

        usine.insert_Produit(nom)
        self.lineEdit_nom_produit.clear()
        self.produits_model.select()
        self.tableView_produits.setColumnHidden(0, True)
        self.load_produits_combo()
        self.load_produits_commande_combo()
        QtWidgets.QMessageBox.information(self, "Succès", f"Produit '{nom}' ajouté !")

    def add_process(self):
        id_produit = self.comboBox_produit.currentData()
        id_machine = self.comboBox_machine_process.currentData()
        ordre = self.spinBox_ordre.value()

        if id_produit is None or id_machine is None:
            QtWidgets.QMessageBox.warning(
                self, "Sélection manquante", "Veuillez sélectionner un produit et une machine."
            )
            return

        if ordre <= 0:
            QtWidgets.QMessageBox.warning(
                self, "Ordre invalide", "L'ordre doit être supérieur à 0."
            )
            return

        usine.insert_Process(id_machine, id_produit, ordre)
        self.load_process_table()
        QtWidgets.QMessageBox.information(self, "Succès", f"Étape {ordre} ajoutée !")

    def load_process_table(self):
        id_produit = self.comboBox_produit.currentData()
        if id_produit is None:
            return

        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT m.nom AS machine, pr.nom AS produit, p.sequence AS ordre
            FROM Process p
            JOIN Machine m ON p.id_machine = m.id_machine
            JOIN Produit pr ON p.id_produit = pr.id_produit
            WHERE p.id_produit = :id_produit
            ORDER BY p.sequence
        """)
        query.bindValue(":id_produit", id_produit)
        query.exec()

        self.process_query_model = QSqlQueryModel()
        self.process_query_model.setQuery(query)
        self.tableView_process.setModel(self.process_query_model)
        self.tableView_process.resizeColumnsToContents()

    # -------------------------------------------------------
    # TAB 3 : COMMANDES
    # -------------------------------------------------------
    def load_produits_commande_combo(self):
        """Charge les produits dans le comboBox de l'onglet Commandes."""
        self.comboBox_produit_commande.clear()
        produits = usine.select_Produit("")
        for p in produits:
            self.comboBox_produit_commande.addItem(p[1], p[0])

    def setup_commandes_table(self):
        """Initialise le tableau des commandes avec les bonnes colonnes."""
        self.tableWidget_commandes.setColumnCount(4)
        self.tableWidget_commandes.setHorizontalHeaderLabels(
            ["Produit", "Heure départ", "Coût estimé (€)", "Statut"]
        )
        self.tableWidget_commandes.horizontalHeader().setStretchLastSection(True)
        self.load_commandes_table()

    def calculer_cout(self):
        """Calcule le coût de production du produit à l'heure choisie."""
        id_produit = self.comboBox_produit_commande.currentData()
        heure_depart = self.timeEdit_depart.time().hour()

        if id_produit is None:
            QtWidgets.QMessageBox.warning(
                self, "Aucun produit", "Veuillez sélectionner un produit."
            )
            return

        # Récupérer le prix de l'électricité à l'heure choisie
        prix_elec = self.get_prix_electricite(heure_depart)

        if prix_elec is None:
            QtWidgets.QMessageBox.warning(
                self, "Prix indisponible",
                f"Pas de prix électricité disponible pour {heure_depart}h.\n"
                "Lancez d'abord import_requests.py pour importer les prix du jour."
            )
            return

        # Calculer le coût total du process pour ce produit
        cout_total = self.calculer_cout_process(id_produit, prix_elec)

        # Afficher le résultat dans le label
        self.label_cout_result.setText(f"Coût estimé : {cout_total:.4f} €")

    def get_prix_electricite(self, heure):
        """Récupère le prix de l'électricité en €/MWh pour une heure donnée."""
        from datetime import date
        aujourd_hui = date.today().strftime("%Y-%m-%d")

        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT prix FROM Electricite
            WHERE date = :date AND heure = :heure
            LIMIT 1
        """)
        query.bindValue(":date", aujourd_hui)
        query.bindValue(":heure", heure)
        query.exec()

        if query.next():
            return query.value(0)
        return None

    def calculer_cout_process(self, id_produit, prix_elec_mwh):
        """
        Calcule le coût total du process pour un produit.
        Formule : (puissance_W / 1000) * (duree_min / 60) * (prix_€/MWh / 1000)
        = coût en €
        """
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT m.puissance, m.duree_cycle
            FROM Process p
            JOIN Machine m ON p.id_machine = m.id_machine
            WHERE p.id_produit = :id_produit
        """)
        query.bindValue(":id_produit", id_produit)
        query.exec()

        cout_total = 0.0
        while query.next():
            puissance_w = query.value(0)    # en Watts
            duree_min = query.value(1)       # en minutes
            # Convertir : W -> kW, min -> h, €/MWh -> €/kWh
            energie_kwh = (puissance_w / 1000) * (duree_min / 60)
            prix_kwh = prix_elec_mwh / 1000
            cout_total += energie_kwh * prix_kwh

        return cout_total

    def valider_commande(self):
        """Valide la commande et l'enregistre dans la DB et le tableau."""
        id_produit = self.comboBox_produit_commande.currentData()
        nom_produit = self.comboBox_produit_commande.currentText()
        heure_depart = self.timeEdit_depart.time().toString("HH:mm")
        heure_int = self.timeEdit_depart.time().hour()

        if id_produit is None:
            QtWidgets.QMessageBox.warning(
                self, "Aucun produit", "Veuillez sélectionner un produit."
            )
            return

        prix_elec = self.get_prix_electricite(heure_int)
        if prix_elec is None:
            cout_str = "N/A"
            cout_val = 0.0
        else:
            cout_val = self.calculer_cout_process(id_produit, prix_elec)
            cout_str = f"{cout_val:.4f} €"

        # Enregistrer dans la DB
        from datetime import date
        aujourd_hui = date.today().strftime("%Y-%m-%d")
        heure_complete = f"{aujourd_hui} {heure_depart}:00"
        usine.insert_Planification(id_produit, 1, heure_complete)

        # Ajouter dans le tableau
        row = self.tableWidget_commandes.rowCount()
        self.tableWidget_commandes.insertRow(row)
        self.tableWidget_commandes.setItem(row, 0, QtWidgets.QTableWidgetItem(nom_produit))
        self.tableWidget_commandes.setItem(row, 1, QtWidgets.QTableWidgetItem(heure_depart))
        self.tableWidget_commandes.setItem(row, 2, QtWidgets.QTableWidgetItem(cout_str))
        self.tableWidget_commandes.setItem(row, 3, QtWidgets.QTableWidgetItem("✅ Validé"))

        QtWidgets.QMessageBox.information(
            self, "Commande validée",
            f"Commande pour '{nom_produit}' à {heure_depart} enregistrée !\nCoût estimé : {cout_str}"
        )

    def load_commandes_table(self):
        """Charge les commandes existantes depuis la DB."""
        query = QtSql.QSqlQuery(self.db)
        query.exec("""
            SELECT pr.nom, pl.heure_debut
            FROM Planification pl
            JOIN Produit pr ON pl.id_produit = pr.id_produit
            ORDER BY pl.heure_debut
        """)

        self.tableWidget_commandes.setRowCount(0)
        while query.next():
            row = self.tableWidget_commandes.rowCount()
            self.tableWidget_commandes.insertRow(row)
            self.tableWidget_commandes.setItem(row, 0, QtWidgets.QTableWidgetItem(query.value(0)))
            self.tableWidget_commandes.setItem(row, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
            self.tableWidget_commandes.setItem(row, 2, QtWidgets.QTableWidgetItem("N/A"))
            self.tableWidget_commandes.setItem(row, 3, QtWidgets.QTableWidgetItem("✅ Validé"))

    # -------------------------------------------------------
    # FERMETURE
    # -------------------------------------------------------
    def closeEvent(self, event):
        if self.db.isOpen():
            self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    usine.createAllTables()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())