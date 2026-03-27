# Module généré par GenDB.py
#===========================
import sqlite3

def createAllTables():
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    # Electricite
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Electricite
            (
                id_electricite INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                heure INTEGER NOT NULL,
                prix REAL NOT NULL,
                quart_d_heure INTEGER NOT NULL
            )
            ''')

    # Commande
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Commande
            (
                id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
                prix REAL NOT NULL,
                date DATE NOT NULL
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

    # Machine
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Machine
            (
                id_machine INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                puissance REAL NOT NULL,
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
                duree_cycle INTEGER NOT NULL,
                FOREIGN KEY (id_machine) REFERENCES Machine(id_machine),
                FOREIGN KEY (id_produit) REFERENCES Produit(id_produit)
            )
            ''')

    # Planification
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Planification
            (
                id_planification INTEGER PRIMARY KEY AUTOINCREMENT,
                id_commande INTEGER NOT NULL,
                id_produit INTEGER NOT NULL,
                moment_utilisation DATETIME NOT NULL,
                FOREIGN KEY (id_commande) REFERENCES Commande(id_commande),
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
                FOREIGN KEY (id_commande) REFERENCES Commande(id_commande),
                FOREIGN KEY (id_electricite) REFERENCES Electricite(id_electricite)
            )
            ''')
    conn.commit()
    conn.close()

# --- INSERTIONS ---

def insert_Operateur(nom, mail):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Operateur (nom, mail) VALUES ('{nom}', '{mail}')"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def insert_Machine(nom, puissance, id_operateur):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Machine (nom, puissance, id_operateur) VALUES ('{nom}', {puissance}, {id_operateur})"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def insert_Produit(nom):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Produit (nom) VALUES ('{nom}')"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def insert_Process(id_machine, id_produit, sequence, duree_cycle):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Process (id_machine, id_produit, sequence, duree_cycle) VALUES ({id_machine}, {id_produit}, {sequence}, {duree_cycle})"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def insert_Electricite(date, heure, prix, quart):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Electricite (date, heure, prix, quart_d_heure) VALUES ('{date}', {heure}, {prix}, {quart})"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def insert_Commande(prix, date):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = f"INSERT OR IGNORE INTO Commande (prix, date) VALUES ({prix}, '{date}')"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

# --- SELECTIONS ---

def select_Operateur(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "SELECT id_operateur, nom, mail FROM Operateur"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    rows = cur.fetchall()
    conn.close()
    return rows

def select_Machine(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "SELECT id_machine, nom, puissance, id_operateur FROM Machine"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    rows = cur.fetchall()
    conn.close()
    return rows

def select_Produit(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "SELECT id_produit, nom FROM Produit"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    rows = cur.fetchall()
    conn.close()
    return rows

def select_Process(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "SELECT id_process, id_machine, id_produit, sequence, duree_cycle FROM Process"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    rows = cur.fetchall()
    conn.close()
    return rows

# --- SUPPRESSIONS ---

def delete_Operateur(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Operateur"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Machine(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Machine"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Produit(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Produit"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Process(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Process"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Electricite(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Electricite"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Commande(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Commande"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()
    
def delete_Consommation(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Consommation"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()

def delete_Planification(WHERE):
    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()
    sqlQuery = "DELETE FROM Planification"
    if WHERE.strip() != "": sqlQuery += f" WHERE {WHERE}"
    cur.execute(sqlQuery)
    conn.commit()
    conn.close()