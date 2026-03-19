from PyQt6 import QtWidgets, QtSql, uic
import sys
import usine


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface_projet.ui", self)

        self.pushButton_add_operateur.clicked.connect(self.add_operateur)
        self.pushButton_add_machine.clicked.connect(self.add_machine)

        self.setup_database()
        self.setup_models()
        self.load_tables()
        self.load_operateurs_combo()

    def setup_database(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("usine.db")

        if not self.db.open():
            QtWidgets.QMessageBox.critical(
                self,
                "Erreur base de données",
                self.db.lastError().text()
            )
            raise RuntimeError("Impossible d'ouvrir la base de données")

    def setup_models(self):
        self.machines_model = QtSql.QSqlRelationalTableModel(self, self.db)
        self.machines_model.setTable("Machine")
        self.tableView_machines.setModel(self.machines_model)

    def load_tables(self):
        if not self.machines_model.select():
            QtWidgets.QMessageBox.critical(
                self,
                "Erreur SQL",
                self.machines_model.lastError().text()
            )

    def load_operateurs_combo(self):
        self.comboBox_operateur.clear()

        operateurs = usine.select_Operateur("")
        for op in operateurs:
            id_operateur = op[0]
            nom_operateur = op[1]

            # texte affiché = nom, donnée cachée = id
            self.comboBox_operateur.addItem(nom_operateur, id_operateur)

    def add_operateur(self):
        nom = self.lineEdit_nom.text().strip()
        mail = self.lineEdit_mail.text().strip()

        if not nom or not mail:
            QtWidgets.QMessageBox.warning(
                self,
                "Champs manquants",
                "Veuillez remplir le nom et l'email."
            )
            return

        usine.insert_Operateur(nom, mail)

        print("Opérateur ajouté !")
        print(usine.select_Operateur(""))

        self.lineEdit_nom.clear()
        self.lineEdit_mail.clear()

        self.load_operateurs_combo()

    def add_machine(self):
        nom = self.lineEdit_nom_machine.text().strip()
        duree = self.lineEdit_duree.text().strip()
        puissance = self.lineEdit_puissance.text().strip()

        if not nom or not duree or not puissance:
            QtWidgets.QMessageBox.warning(
                self,
                "Champs manquants",
                "Veuillez remplir tous les champs de la machine."
            )
            return

        try:
            duree = int(duree)
            puissance = float(puissance)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Valeurs invalides",
                "Durée doit être un entier et puissance un nombre."
            )
            return

        id_op = self.comboBox_operateur.currentData()

        if id_op is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Aucun opérateur",
                "Veuillez d'abord ajouter un opérateur."
            )
            return

        usine.insert_Machine(nom, duree, puissance, id_op)

        print("Machine ajoutée !")
        print(usine.select_Machine(""))

        self.lineEdit_nom_machine.clear()
        self.lineEdit_duree.clear()
        self.lineEdit_puissance.clear()

        self.load_tables()

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