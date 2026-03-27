from PyQt6 import QtWidgets, QtSql, uic
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQueryModel
import sys
import usine
import mail
from datetime import date

# Héritage de QWidget car ton fichier .ui est un Form/QWidget
class MainWindow(QtWidgets.QWidget): 
    def __init__(self):
        super().__init__()
        uic.loadUi("interface_projet.ui", self)

        # Plein écran
        self.showMaximized() 
        
        # Date du jour
        aujourd_hui_str = date.today().strftime("%d/%m/%Y")
        self.label_date_aujourdhui.setText(f"Date du jour : {aujourd_hui_str}")
        self.label_date_aujourdhui_2.setText(f"Date du jour : {aujourd_hui_str}")
        self.label_date_aujourdhui_3.setText(f"Date du jour : {aujourd_hui_str}")

        # Ajustement colonnes tableaux
        self.tableView_machines.horizontalHeader().setStretchLastSection(True)
        self.tableView_produits.horizontalHeader().setStretchLastSection(True)
        self.tableView_process.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_commandes.horizontalHeader().setStretchLastSection(True)

        self.commande_en_cours = []

        # Connexions
        self.pushButton_add_operateur.clicked.connect(self.add_operateur)
        self.pushButton_delete_operateur.clicked.connect(self.delete_operateur)
        self.pushButton_add_machine.clicked.connect(self.add_machine)
        self.pushButton_delete_machine.clicked.connect(self.delete_machine)
        self.pushButton_add_produit.clicked.connect(self.add_produit)
        self.pushButton_add_process.clicked.connect(self.add_process)
        self.comboBox_produit.currentIndexChanged.connect(self.load_process_table)
        self.pushButton_calculer.clicked.connect(self.calculer_cout)
        self.pushButton_ajouter_produit_commande.clicked.connect(self.ajouter_produit_commande)
        self.pushButton_valider_commande.clicked.connect(self.valider_commande)
        self.pushButton_delete_produit.clicked.connect(self.delete_produit)
        
        # Nouvelles connexions pour les étapes
        if hasattr(self, 'pushButton_delete_step'):
            self.pushButton_delete_step.clicked.connect(self.delete_step)
        if hasattr(self, 'pushButton_edit_step'):
            self.pushButton_edit_step.clicked.connect(self.edit_step)

        # Init
        self.setup_database()
        self.setup_models()
        self.load_tables()
        self.load_operateurs_combo()
        self.load_produits_combo()
        self.load_machines_combo()
        self.load_produits_commande_combo()
        self.setup_commandes_table()

    def setup_database(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("usine.db")
        if not self.db.open():
            QtWidgets.QMessageBox.critical(self, "Erreur", self.db.lastError().text())
            raise RuntimeError("Base de données inaccessible")

    def setup_models(self):
        self.produits_model = QtSql.QSqlRelationalTableModel(self, self.db)
        self.produits_model.setTable("Produit")
        self.produits_model.select()
        self.tableView_produits.setModel(self.produits_model)

    def load_tables(self):
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT m.id_machine, m.nom, m.puissance, o.nom, o.mail 
            FROM Machine m 
            JOIN Operateur o ON m.id_operateur = o.id_operateur
        """)
        query.exec()
        
        self.machines_display_model = QtSql.QSqlQueryModel()
        self.machines_display_model.setQuery(query)
        
        self.machines_display_model.setHeaderData(1, Qt.Orientation.Horizontal, "Nom Machine")
        self.machines_display_model.setHeaderData(2, Qt.Orientation.Horizontal, "Puissance (W)")
        self.machines_display_model.setHeaderData(3, Qt.Orientation.Horizontal, "Opérateur")
        self.machines_display_model.setHeaderData(4, Qt.Orientation.Horizontal, "Email")

        self.tableView_machines.setModel(self.machines_display_model)
        self.tableView_machines.setColumnHidden(0, True)
        
        self.produits_model.select()
        self.tableView_produits.setColumnHidden(0, True)

    def load_operateurs_combo(self):
        self.comboBox_operateur.clear()
        for op in usine.select_Operateur(""):
            self.comboBox_operateur.addItem(op[1], op[0])

    def add_operateur(self):
        nom, email = self.lineEdit_nom.text().strip(), self.lineEdit_mail.text().strip()
        if nom and email:
            usine.insert_Operateur(nom, email)
            self.lineEdit_nom.clear(); self.lineEdit_mail.clear()
            self.load_operateurs_combo()

    def delete_operateur(self):
        id_op = self.comboBox_operateur.currentData()
        nom_op = self.comboBox_operateur.currentText()
        if id_op:
            query = QtSql.QSqlQuery(self.db)
            query.prepare("SELECT nom FROM Machine WHERE id_operateur = :id")
            query.bindValue(":id", id_op)
            query.exec()
            machines_liees = []
            while query.next(): machines_liees.append(query.value(0))
            if machines_liees:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Cet opérateur a encore des machines.")
                return
            if QtWidgets.QMessageBox.question(self, "Confirmer", f"Supprimer {nom_op} ?") == QtWidgets.QMessageBox.StandardButton.Yes:
                usine.delete_Operateur(f"id_operateur = {id_op}")
                self.load_operateurs_combo()
                self.load_tables()

    def add_machine(self):
        nom = self.lineEdit_nom_machine.text().strip()
        try:
            puissance = float(self.lineEdit_puissance.text())
            id_op = self.comboBox_operateur.currentData()
            if nom and id_op:
                usine.insert_Machine(nom, puissance, id_op)
                self.load_tables() 
                self.load_machines_combo()
        except ValueError: 
            QtWidgets.QMessageBox.warning(self, "Erreur", "Puissance invalide")
            
    def delete_machine(self):
        index = self.tableView_machines.currentIndex()
        if not index.isValid(): return
        row = index.row()
        id_m = self.machines_display_model.index(row, 0).data()
        if QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer cette machine ?") == QtWidgets.QMessageBox.StandardButton.Yes:
            usine.delete_Machine(f"id_machine = {id_m}")
            self.load_tables()
            self.load_machines_combo()

    def load_produits_combo(self):
        self.comboBox_produit.clear()
        for p in usine.select_Produit(""):
            self.comboBox_produit.addItem(p[1], p[0])
        self.load_process_table()

    def load_machines_combo(self):
        self.comboBox_machine_process.clear()
        for m in usine.select_Machine(""):
            self.comboBox_machine_process.addItem(m[1], m[0])

    def add_produit(self):
        nom = self.lineEdit_nom_produit.text().strip()
        if nom:
            usine.insert_Produit(nom)
            self.load_tables()
            self.load_produits_combo()
            self.load_produits_commande_combo()

    def delete_produit(self):
        index = self.tableView_produits.currentIndex()
        if not index.isValid(): return
        row = index.row()
        id_p = self.produits_model.index(row, 0).data()
        if QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer ce produit et son process ?") == QtWidgets.QMessageBox.StandardButton.Yes:
            usine.delete_Process(f"id_produit = {id_p}")
            usine.delete_Produit(f"id_produit = {id_p}")
            self.load_tables()
            self.load_produits_combo()
            self.load_produits_commande_combo()

    def add_process(self):
        id_p = self.comboBox_produit.currentData()
        id_m = self.comboBox_machine_process.currentData()
        ordre = self.spinBox_ordre.value()
        try:
            duree = self.spinBox_duree_process.value() 
        except AttributeError: return
        if id_p and id_m and duree > 0:
            usine.insert_Process(id_m, id_p, ordre, duree)
            self.load_process_table()

    def load_process_table(self):
        id_p = self.comboBox_produit.currentData()
        if not id_p: return
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT p.id_machine, p.id_produit, m.nom, pr.nom, p.sequence, p.duree_cycle 
            FROM Process p 
            JOIN Machine m ON p.id_machine = m.id_machine 
            JOIN Produit pr ON p.id_produit = pr.id_produit 
            WHERE p.id_produit = :id 
            ORDER BY p.sequence
        """)
        query.bindValue(":id", id_p); query.exec()
        self.process_query_model = QSqlQueryModel()
        self.process_query_model.setQuery(query)
        self.tableView_process.setModel(self.process_query_model)
        self.tableView_process.setColumnHidden(0, True) # Cache ID Machine
        self.tableView_process.setColumnHidden(1, True) # Cache ID Produit
        self.process_query_model.setHeaderData(2, Qt.Orientation.Horizontal, "Machine")
        self.process_query_model.setHeaderData(3, Qt.Orientation.Horizontal, "Produit")
        self.process_query_model.setHeaderData(4, Qt.Orientation.Horizontal, "Ordre")
        self.process_query_model.setHeaderData(5, Qt.Orientation.Horizontal, "Durée (min)")

    def delete_step(self):
        index = self.tableView_process.currentIndex()
        if not index.isValid(): return
        row = index.row()
        id_m = self.process_query_model.index(row, 0).data()
        id_p = self.process_query_model.index(row, 1).data()
        seq = self.process_query_model.index(row, 4).data()
        if QtWidgets.QMessageBox.question(self, "Confirmer", "Supprimer cette étape ?") == QtWidgets.QMessageBox.StandardButton.Yes:
            usine.delete_Process(f"id_machine = {id_m} AND id_produit = {id_p} AND sequence = {seq}")
            self.load_process_table()

    def edit_step(self):
        index = self.tableView_process.currentIndex()
        if not index.isValid(): return
        row = index.row()
        id_m = self.process_query_model.index(row, 0).data()
        id_p = self.process_query_model.index(row, 1).data()
        old_seq = self.process_query_model.index(row, 4).data()
        new_seq = self.spinBox_ordre.value()
        new_dur = self.spinBox_duree_process.value()
        query = QtSql.QSqlQuery(self.db)
        query.prepare("UPDATE Process SET sequence = :s, duree_cycle = :d WHERE id_machine = :m AND id_produit = :p AND sequence = :os")
        query.bindValue(":s", new_seq); query.bindValue(":d", new_dur)
        query.bindValue(":m", id_m); query.bindValue(":p", id_p); query.bindValue(":os", old_seq)
        if query.exec(): self.load_process_table()

    def load_produits_commande_combo(self):
        self.comboBox_produit_commande.clear()
        for p in usine.select_Produit(""):
            self.comboBox_produit_commande.addItem(p[1], p[0])

    def setup_commandes_table(self):
        self.tableWidget_commandes.setColumnCount(4)
        self.tableWidget_commandes.setHorizontalHeaderLabels(["Produit", "Heure départ", "Coût (€)", "Statut"])

    def get_prix_electricite(self, heure):
        q = QtSql.QSqlQuery(self.db)
        q.prepare("SELECT prix FROM Electricite WHERE date = :d AND heure = :h LIMIT 1")
        q.bindValue(":d", date.today().strftime("%Y-%m-%d")); q.bindValue(":h", heure); q.exec()
        return q.value(0) if q.next() else None

    def calculer_cout_process(self, id_p, heure_depart):
        query = QtSql.QSqlQuery(self.db)
        query.prepare("""
            SELECT m.puissance, p.duree_cycle FROM Process p 
            JOIN Machine m ON p.id_machine = m.id_machine 
            WHERE p.id_produit = :id ORDER BY p.sequence
        """)
        query.bindValue(":id", id_p); query.exec()
        total_cout, minutes_cumulees, heure_actuelle = 0.0, self.timeEdit_depart.time().minute(), heure_depart
        while query.next():
            puis, dur = query.value(0), query.value(1)
            prix_mwh = self.get_prix_electricite(heure_actuelle) or 0.0
            total_cout += (puis / 1000) * (dur / 60) * (prix_mwh / 1000)
            minutes_cumulees += dur
            while minutes_cumulees >= 60:
                minutes_cumulees -= 60
                heure_actuelle = (heure_actuelle + 1) % 24
        return total_cout

    def calculer_cout(self):
        id_p = self.comboBox_produit_commande.currentData()
        h_dep = self.timeEdit_depart.time().hour()
        if id_p:
            total = self.calculer_cout_process(id_p, h_dep)
            self.label_cout_result.setText(f"Coût : {total:.4f} €")

    def ajouter_produit_commande(self):
        id_p = self.comboBox_produit_commande.currentData()
        if not id_p: return
        nom, h_time = self.comboBox_produit_commande.currentText(), self.timeEdit_depart.time()
        cout = self.calculer_cout_process(id_p, h_time.hour())
        self.commande_en_cours.append({"id_produit": id_p, "nom": nom, "heure": h_time.toString("HH:mm"), "cout": cout})
        row = self.tableWidget_commandes.rowCount()
        self.tableWidget_commandes.insertRow(row)
        self.tableWidget_commandes.setItem(row, 0, QtWidgets.QTableWidgetItem(nom))
        self.tableWidget_commandes.setItem(row, 1, QtWidgets.QTableWidgetItem(h_time.toString("HH:mm")))
        self.tableWidget_commandes.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{cout:.4f} €"))
        self.tableWidget_commandes.setItem(row, 3, QtWidgets.QTableWidgetItem("⏳ En attente"))
        self.update_prix_total()

    def update_prix_total(self):
        total = sum(p["cout"] for p in self.commande_en_cours)
        self.label_cout_total.setText(f"Total : {total:.4f} €")

    def valider_commande(self):
        if not self.commande_en_cours: return
        usine.insert_Commande(sum(p['cout'] for p in self.commande_en_cours), date.today().strftime("%Y-%m-%d"))
        mail.envoyer_mails_commande(self.db, self.commande_en_cours)
        self.commande_en_cours = []
        self.tableWidget_commandes.setRowCount(0)
        self.update_prix_total()
        QtWidgets.QMessageBox.information(self, "Succès", "Commande validée !")

    def closeEvent(self, event):
        if hasattr(self, 'db') and self.db.isOpen(): self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    usine.createAllTables()
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 