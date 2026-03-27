import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------
EMAIL_EXPEDITEUR = "walid.abdelk05@gmail.com"
MOT_DE_PASSE = "hsoz ynnc kjgr xkqx"

def envoyer_mail(destinataire, nom_op, nom_machine, nom_produit, heure_debut, duree):
    """
    Envoie un mail à un opérateur pour lui décrire sa tâche.
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
    Envoie les mails à tous les opérateurs pour une commande en calculant
    les horaires séquentiels basés sur la durée spécifique de chaque étape.
    """
    from PyQt6 import QtSql

    mails_envoyes = 0

    for produit in produits_commande:
        id_produit = produit["id_produit"]
        heure = produit["heure"]
        nom_produit = produit["nom"]

        # MODIFICATION : On récupère p.duree_cycle au lieu de m.duree_cycle
        query = QtSql.QSqlQuery(db)
        query.prepare("""
            SELECT m.nom, p.duree_cycle, op.nom, op.mail, p.sequence
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
        temps_courant = h * 60 + m  # minutes depuis minuit

        while query.next():
            nom_machine = query.value(0)
            duree = query.value(1) # Durée spécifique au produit sur cette machine
            nom_op = query.value(2)
            mail_op = query.value(3)

            # Formatage de l'heure de début pour cet opérateur
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

            # Avancer le temps pour la prochaine étape de la séquence
            temps_courant += duree

    return mails_envoyes


def envoyer_alerte_prix_negatif(destinataire, image_bytes):
    """
    Envoie un mail d'alerte contenant le graphique des prix de la journée.
    """
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_EXPEDITEUR
    msg["To"] = destinataire
    msg["Subject"] = "⚠️ ALERTE : Prix de l'électricité négatifs détectés"

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
    
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(corps_html, "html"))

    image = MIMEImage(image_bytes, name="graphique_prix.png")
    image.add_header('Content-ID', '<graphique_prix>')
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