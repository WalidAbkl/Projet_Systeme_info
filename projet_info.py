# Module g�n�r� par GenDB.py
#===========================
import sqlite3
from PySide6.QtSql import QSqlDatabase, QSqlTableModel

def createAllTables():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commande
			(
				id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
				Prix REAL NOT NULL,
				date TEXT NOT NULL
			)
			''')

	# electricite
	cur.execute('''
			CREATE TABLE IF NOT EXISTS electricite
			(
				id_electricite INTEGER PRIMARY KEY AUTOINCREMENT,
				date TEXT NOT NULL,
				heure TEXT NOT NULL,
				Prix REAL NOT NULL,
				quart_d_heure INTEGER NOT NULL
			)
			''')

	# Produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Produit
			(
				id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL
			)
			''')

	# Operateur
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Operateur
			(
				id_operateur INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				mail TEXT UNIQUE NOT NULL
			)
			''')

	# Planification
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Planification
			(
				id_planification INTEGER PRIMARY KEY AUTOINCREMENT,
				id_commande INTEGER NOT NULL,
				id_produit INTEGER NOT NULL,
				moment_d_utilisation INTEGER NOT NULL,
				FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
				FOREIGN KEY (id_produit) REFERENCES Produit(id_produit)
			)
			''')

	# Consommation
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Consommation
			(
				id_consommation INTEGER PRIMARY KEY AUTOINCREMENT,
				id_commande INTEGER NOT NULL,
				id_electricite INTEGER NOT NULL,
				FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
				FOREIGN KEY (id_electricite) REFERENCES electricite(id_electricite)
			)
			''')

	# Machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Machine
			(
				id_machine INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				Duree_du_cycle REAL NOT NULL,
				Puissance INTEGER NOT NULL,
				id_operateur INTEGER NOT NULL,
				FOREIGN KEY (id_operateur) REFERENCES Operateur(id_operateur)
			)
			''')

	# Process
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Process
			(
				id_process INTEGER PRIMARY KEY AUTOINCREMENT,
				id_machine INTEGER NOT NULL,
				id_produit INTEGER NOT NULL,
				sequence INTEGER NOT NULL,
				FOREIGN KEY (id_machine) REFERENCES Machine(id_machine),
				FOREIGN KEY (id_produit) REFERENCES Produit(id_produit)
			)
			''')
	conn.commit()
	conn.close()

def createTables_commande():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commande
			(
				id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
				Prix REAL NOT NULL,
				date TEXT NOT NULL
			)
			''')
	conn.commit()
	conn.close()

def createTables_electricite():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# electricite
	cur.execute('''
			CREATE TABLE IF NOT EXISTS electricite
			(
				id_electricite INTEGER PRIMARY KEY AUTOINCREMENT,
				date TEXT NOT NULL,
				heure TEXT NOT NULL,
				Prix REAL NOT NULL,
				quart_d_heure INTEGER NOT NULL
			)
			''')
	conn.commit()
	conn.close()

def createTables_Produit():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Produit
			(
				id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL
			)
			''')
	conn.commit()
	conn.close()

def createTables_Operateur():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Operateur
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Operateur
			(
				id_operateur INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				mail TEXT UNIQUE NOT NULL
			)
			''')
	conn.commit()
	conn.close()

def createTables_Planification():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Planification
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Planification
			(
				id_planification INTEGER PRIMARY KEY AUTOINCREMENT,
				id_commande INTEGER NOT NULL,
				id_produit INTEGER NOT NULL,
				moment_d_utilisation INTEGER NOT NULL,
				FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
				FOREIGN KEY (id_produit) REFERENCES Produit(id_produit)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Consommation():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Consommation
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Consommation
			(
				id_consommation INTEGER PRIMARY KEY AUTOINCREMENT,
				id_commande INTEGER NOT NULL,
				id_electricite INTEGER NOT NULL,
				FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
				FOREIGN KEY (id_electricite) REFERENCES electricite(id_electricite)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Machine():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Machine
			(
				id_machine INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				Duree_du_cycle REAL NOT NULL,
				Puissance INTEGER NOT NULL,
				id_operateur INTEGER NOT NULL,
				FOREIGN KEY (id_operateur) REFERENCES Operateur(id_operateur)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Process():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	# Process
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Process
			(
				id_process INTEGER PRIMARY KEY AUTOINCREMENT,
				id_machine INTEGER NOT NULL,
				id_produit INTEGER NOT NULL,
				sequence INTEGER NOT NULL,
				FOREIGN KEY (id_machine) REFERENCES Machine(id_machine),
				FOREIGN KEY (id_produit) REFERENCES Produit(id_produit)
			)
			''')
	conn.commit()
	conn.close()

# INSERT INTO commande
def insert_commande(Prix,date):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO commande (Prix,date) "
	sqlQuery+=f"VALUES ({Prix},'{date}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO electricite
def insert_electricite(date,heure,Prix,quart_d_heure):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO electricite (date,heure,Prix,quart_d_heure) "
	sqlQuery+=f"VALUES ('{date}','{heure}',{Prix},{quart_d_heure})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Produit
def insert_Produit(nom):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Produit (nom) "
	sqlQuery+=f"VALUES ('{nom}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Operateur
def insert_Operateur(nom,mail):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Operateur (nom,mail) "
	sqlQuery+=f"VALUES ('{nom}','{mail}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Planification
def insert_Planification(id_commande,id_produit,moment_d_utilisation):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Planification (id_commande,id_produit,moment_d_utilisation) "
	sqlQuery+=f"VALUES ({id_commande},{id_produit},{moment_d_utilisation})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Consommation
def insert_Consommation(id_commande,id_electricite):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Consommation (id_commande,id_electricite) "
	sqlQuery+=f"VALUES ({id_commande},{id_electricite})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Machine
def insert_Machine(nom,Duree_du_cycle,Puissance,id_operateur):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Machine (nom,Duree_du_cycle,Puissance,id_operateur) "
	sqlQuery+=f"VALUES ('{nom}',{Duree_du_cycle},{Puissance},{id_operateur})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Process
def insert_Process(id_machine,id_produit,sequence):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Process (id_machine,id_produit,sequence) "
	sqlQuery+=f"VALUES ({id_machine},{id_produit},{sequence})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# SELECT fields FROM commande WHERE condition
def select_commande(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_commande,Prix,date FROM commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM electricite WHERE condition
def select_electricite(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_electricite,date,heure,Prix,quart_d_heure FROM electricite"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Produit WHERE condition
def select_Produit(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_produit,nom FROM Produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Operateur WHERE condition
def select_Operateur(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_operateur,nom,mail FROM Operateur"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Planification WHERE condition
def select_Planification(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_planification,id_commande,id_produit,moment_d_utilisation FROM Planification"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Consommation WHERE condition
def select_Consommation(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_consommation,id_commande,id_electricite FROM Consommation"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Machine WHERE condition
def select_Machine(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_machine,nom,Duree_du_cycle,Puissance,id_operateur FROM Machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Process WHERE condition
def select_Process(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_process,id_machine,id_produit,sequence FROM Process"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# UPDATE commande SET fields=value WHERE condition
def update_commande(id_commande,Prix,date,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE commande SET id_commande = {id_commande},Prix = {Prix},date='{date}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE electricite SET fields=value WHERE condition
def update_electricite(id_electricite,date,heure,Prix,quart_d_heure,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE electricite SET id_electricite = {id_electricite},date='{date}',heure='{heure}',Prix = {Prix},quart_d_heure = {quart_d_heure}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Produit SET fields=value WHERE condition
def update_Produit(id_produit,nom,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Produit SET id_produit = {id_produit},nom='{nom}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Operateur SET fields=value WHERE condition
def update_Operateur(id_operateur,nom,mail,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Operateur SET id_operateur = {id_operateur},nom='{nom}',mail='{mail}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Planification SET fields=value WHERE condition
def update_Planification(id_planification,id_commande,id_produit,moment_d_utilisation,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Planification SET id_planification = {id_planification},id_commande = {id_commande},id_produit = {id_produit},moment_d_utilisation = {moment_d_utilisation}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Consommation SET fields=value WHERE condition
def update_Consommation(id_consommation,id_commande,id_electricite,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Consommation SET id_consommation = {id_consommation},id_commande = {id_commande},id_electricite = {id_electricite}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Machine SET fields=value WHERE condition
def update_Machine(id_machine,nom,Duree_du_cycle,Puissance,id_operateur,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Machine SET id_machine = {id_machine},nom='{nom}',Duree_du_cycle = {Duree_du_cycle},Puissance = {Puissance},id_operateur = {id_operateur}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Process SET fields=value WHERE condition
def update_Process(id_process,id_machine,id_produit,sequence,WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Process SET id_process = {id_process},id_machine = {id_machine},id_produit = {id_produit},sequence = {sequence}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM commande WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_commande(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM electricite WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_electricite(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM electricite"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Produit WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Produit(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Operateur WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Operateur(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Operateur"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Planification WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Planification(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Planification"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Consommation WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Consommation(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Consommation"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Machine WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Machine(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Process WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les donn�es de la table !!!
def delete_Process(WHERE):
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Process"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE commande
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_commande():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE commande"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE electricite
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_electricite():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE electricite"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Produit
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Produit():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Produit"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Operateur
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Operateur():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Operateur"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Planification
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Planification():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Planification"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Consommation
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Consommation():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Consommation"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Machine
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Machine():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Machine"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Process
# ATTENTION : cette fonction d�truit la table, elle devra (�ventuellement) �tre recr��e
def drop_Process():
	conn = sqlite3.connect("projet_info.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Process"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

