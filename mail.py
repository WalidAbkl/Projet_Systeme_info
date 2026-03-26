import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  # <-- NOUVEL IMPORT POUR L'IMAGE

# -------------------------------------------------------
# CONFIGURATION - Mets tes infos ici
# -------------------------------------------------------
EMAIL_EXPEDITEUR = "walid.abdelk05@gmail.com"   # ← ton Gmail
MOT_DE_PASSE = "hsoz ynnc kjgr xkqx"       # ← mot de passe d'application


def envoyer_mail(destinataire, nom_op, nom_machine, nom_produit, heure_debut, duree):
    """
    Envoie un mail à un opérateur pour lui décrire sa tâche.
    
    Args:
        destinataire : adresse mail de l'opérateur
        nom_op       : nom de l'opérateur
        nom_machine  : nom de la machine à utiliser
        nom_produit  : nom du produit à fabriquer
        heure_debut  : heure de début de la tâche (format "HH:MM")
        duree        : durée de la tâche en minutes
    """
    msg = MIMEMultipart()
    msg["From"] = EMAIL_EXPEDITEUR
    msg["To"] = destinataire
    msg["Subject"] = f"Tâche assignée - {nom_machine}"

    corps = f"""
Bonjour {nom_op},

Vous avez une tâche assignée aujourd'hui :

- Machine     : {nom_machine}
- Produit     : {nom_produit}
- Heure début : {heure_debut}
- Durée       : {duree} minutes

Bonne journée !
    """
    msg.attach(MIMEText(corps, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            server.send_message(msg)
        print(f"✅ Mail envoyé à {nom_op} ({destinataire})")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi mail à {destinataire} : {e}")
        return False


def envoyer_mails_commande(db, produits_commande):
    """
    Envoie les mails à tous les opérateurs pour une commande.
    
    Args:
        db               : connexion QtSql à la DB
        produits_commande: liste de dicts avec id_produit, nom, heure, cout
    """
    from PyQt6 import QtSql

    mails_envoyes = 0

    for produit in produits_commande:
        id_produit = produit["id_produit"]
        heure = produit["heure"]
        nom_produit = produit["nom"]

        # Récupérer les machines et opérateurs du process dans l'ordre
        query = QtSql.QSqlQuery(db)
        query.prepare("""
            SELECT m.nom, m.duree_cycle, op.nom, op.mail, p.sequence
            FROM Process p
            JOIN Machine m ON p.id_machine = m.id_machine
            JOIN Operateur op ON m.id_operateur = op.id_operateur
            WHERE p.id_produit = :id_produit
            ORDER BY p.sequence
        """)
        query.bindValue(":id_produit", id_produit)
        query.exec()

        # Calculer les heures de départ de chaque étape
        h, m = map(int, heure.split(":"))
        temps_courant = h * 60 + m  # en minutes depuis minuit

        while query.next():
            nom_machine = query.value(0)
            duree = query.value(1)
            nom_op = query.value(2)
            mail_op = query.value(3)

            heure_debut = f"{temps_courant // 60:02d}:{temps_courant % 60:02d}"

            succes = envoyer_mail(
                destinataire=mail_op,
                nom_op=nom_op,
                nom_machine=nom_machine,
                nom_produit=nom_produit,
                heure_debut=heure_debut,
                duree=duree
            )

            if succes:
                mails_envoyes += 1

            # Avancer le temps pour la prochaine étape
            temps_courant += duree

    return mails_envoyes


# -------------------------------------------------------
# NOUVELLE FONCTION : ALERTE PRIX NÉGATIF (GRAPHIQUE)
# -------------------------------------------------------
def envoyer_alerte_prix_negatif(destinataire, image_bytes):
    """
    Envoie un mail d'alerte contenant le graphique des prix de la journée.
    """
    # Utilisation de 'related' pour pouvoir intégrer l'image inline dans le code HTML
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_EXPEDITEUR
    msg["To"] = destinataire
    msg["Subject"] = "⚠️ ALERTE : Prix de l'électricité négatifs détectés"

    # Construction du corps du mail en HTML avec la balise img faisant référence au CID
    corps_html = """
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Bonjour,</p>
        <p>Le système automatique a détecté une opportunité pour aujourd'hui : des prix d'électricité <b>négatifs</b> sont prévus.</p>
        <p>Voici le graphique récapitulatif des prix de la journée (les valeurs négatives sont en rouge) :</p>
        
        <br>
        <img src="cid:graphique_prix" alt="Graphique des prix">
        <br>
        
        <p>Il est fortement conseillé de planifier la production durant ces intervalles pour optimiser les coûts.</p>
        <p>Cordialement,<br>Le système de gestion d'usine.</p>
    </body>
    </html>
    """
    
    # On attache le texte HTML
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(corps_html, "html"))

    # On prépare et on attache l'image graphique
    image = MIMEImage(image_bytes, name="graphique_prix.png")
    image.add_header('Content-ID', '<graphique_prix>') # Fait le lien avec le <img src="cid:... ">
    image.add_header('Content-Disposition', 'inline', filename='graphique_prix.png')
    msg.attach(image)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            server.send_message(msg)
        print(f"✅ Alerte graphique envoyée à {destinataire}")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi alerte à {destinataire} : {e}")
        return False