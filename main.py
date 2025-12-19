# ====================================================================
# APPLICATION RECONNAISSANCE FACIALE - RESTAURANT SCOLAIRE
# ====================================================================

# Importer OpenCV pour la webcam et la reconnaissance faciale
import cv2
# Importer le module os pour créer/gérer des dossiers
import os
# Importer numpy pour les calculs mathématiques
import numpy as np
# Importer tkinter pour faire l'interface graphique
from tkinter import *
# Importer messagebox pour afficher des messages
from tkinter import messagebox
# Importer json pour sauvegarder les soldes dans un fichier
import json


# ====================================================================
# FONCTION 1 : Créer les dossiers nécessaires
# ====================================================================

def creer_dossiers():
    # Créer le dossier "data" s'il n'existe pas
    if not os.path.exists("data"):
        os.makedirs("data")
    # Afficher un message pour confirmer
    print("✓ Dossier 'data' créé ou trouvé")


# ====================================================================
# FONCTION 1B : Créer le fichier des soldes
# ====================================================================

def creer_fichier_soldes():
    # Vérifier si le fichier soldes.json existe
    if not os.path.exists("soldes.json"):
        # Créer un dictionnaire vide
        soldes = {}
        # Sauvegarder dans le fichier
        with open("soldes.json", "w") as f:
            json.dump(soldes, f)
    # Afficher un message pour confirmer
    print("✓ Fichier 'soldes.json' créé ou trouvé")


# ====================================================================
# FONCTION 2 : Interface principale
# ====================================================================

def interface_principale():
    # Créer la fenêtre principale
    fenetre = Tk()
    # Donner un titre à la fenêtre
    fenetre.title("Restaurant - Reconnaissance Faciale")
    # Donner une taille à la fenêtre (largeur x hauteur)
    fenetre.geometry("400x300")
    # Donner une couleur de fond
    fenetre.configure(bg="lightblue")
    
    # Créer un titre avec du texte gros et gras
    titre = Label(
        fenetre,
        text="RESTAURANT SCOLAIRE",
        font=("Arial", 20, "bold"),
        bg="lightblue"
    )
    # Placer le titre en haut de la fenêtre
    titre.pack(pady=20)
    
    # Créer un sous-titre
    sous_titre = Label(
        fenetre,
        text="Choisissez une option:",
        font=("Arial", 14),
        bg="lightblue"
    )
    # Placer le sous-titre
    sous_titre.pack(pady=10)
    
    # Créer le bouton "Administrateur"
    btn_admin = Button(
        fenetre,
        text="👤 ADMINISTRATEUR",
        font=("Arial", 12, "bold"),
        bg="orange",
        fg="white",
        width=30,
        # Quand on clique, appeler la fonction authentifier_admin
        command=authentifier_admin
    )
    # Placer le bouton
    btn_admin.pack(pady=15)
    
    # Créer le bouton "M'identifier"
    btn_identifier = Button(
        fenetre,
        text="✓ M'IDENTIFIER",
        font=("Arial", 12, "bold"),
        bg="green",
        fg="white",
        width=30,
        # Quand on clique, appeler la fonction interface_identification
        command=interface_identification
    )
    # Placer le bouton
    btn_identifier.pack(pady=15)
    
    # Lancer la fenêtre (elle reste active jusqu'à qu'on la ferme)
    fenetre.mainloop()


# ====================================================================
# FONCTION 3 : Authentifier l'administrateur
# ====================================================================

def authentifier_admin():
    # Créer une fenêtre pour la connexion
    fenetre_login = Toplevel()
    # Donner un titre
    fenetre_login.title("Connexion Administrateur")
    # Donner une taille
    fenetre_login.geometry("300x200")
    # Couleur de fond
    fenetre_login.configure(bg="lightyellow")
    
    # Titre
    titre = Label(
        fenetre_login,
        text="AUTHENTIFICATION",
        font=("Arial", 12, "bold"),
        bg="lightyellow"
    )
    titre.pack(pady=10)
    
    # Label pour l'identifiant
    label_id = Label(
        fenetre_login,
        text="Identifiant:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_id.pack(pady=5)
    
    # Zone pour entrer l'identifiant
    entree_id = Entry(fenetre_login, font=("Arial", 11), width=25)
    entree_id.pack(pady=5)
    
    # Label pour le mot de passe
    label_pass = Label(
        fenetre_login,
        text="Mot de passe:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_pass.pack(pady=5)
    
    # Zone pour entrer le mot de passe (avec des points)
    entree_pass = Entry(fenetre_login, font=("Arial", 11), width=25, show="*")
    entree_pass.pack(pady=5)
    
    # Fonction pour vérifier les identifiants
    def verifier_login():
        # Récupérer l'identifiant et le mot de passe
        id_admin = entree_id.get()
        pass_admin = entree_pass.get()
        
        # Vérifier que c'est correct (admin / admin)
        if id_admin == "admin" and pass_admin == "admin":
            # Fermer la fenêtre de login
            fenetre_login.destroy()
            # Ouvrir l'interface admin
            interface_admin()
        else:
            # Afficher un message d'erreur
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect!")
    
    # Bouton pour se connecter
    btn_connexion = Button(
        fenetre_login,
        text="Connexion",
        font=("Arial", 11),
        bg="orange",
        fg="white",
        width=20,
        command=verifier_login
    )
    btn_connexion.pack(pady=10)


# ====================================================================
# FONCTION 4 : Interface Administrateur
# ====================================================================

def interface_admin():
    # Créer une nouvelle fenêtre pour l'administrateur
    fenetre_admin = Toplevel()
    # Donner un titre
    fenetre_admin.title("Administrateur")
    # Donner une taille
    fenetre_admin.geometry("400x300")
    # Couleur de fond
    fenetre_admin.configure(bg="lightyellow")
    
    # Titre
    titre = Label(
        fenetre_admin,
        text="INTERFACE ADMINISTRATEUR",
        font=("Arial", 14, "bold"),
        bg="lightyellow"
    )
    titre.pack(pady=10)
    
    # Label "Nom de la personne"
    label_nom = Label(
        fenetre_admin,
        text="Nom de la personne:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_nom.pack(pady=5)
    
    # Zone où on peut taper le nom (Entry = zone de texte)
    entree_nom = Entry(fenetre_admin, font=("Arial", 11), width=30)
    entree_nom.pack(pady=5)
    
    # Label "Solde initial"
    label_solde = Label(
        fenetre_admin,
        text="Solde initial (€):",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_solde.pack(pady=5)
    
    # Zone pour le solde
    entree_solde = Entry(fenetre_admin, font=("Arial", 11), width=30)
    entree_solde.insert(0, "50")
    entree_solde.pack(pady=5)
    
    # Fonction pour ajouter une personne
    def ajouter_personne():
        # Récupérer le nom tapé
        nom = entree_nom.get().strip()
        # Récupérer le solde
        solde = entree_solde.get().strip()
        # Vérifier que le nom n'est pas vide
        if nom == "":
            # Afficher une erreur si le nom est vide
            messagebox.showerror("Erreur", "Veuillez entrer un nom!")
        else:
            # Appeler la fonction pour ajouter la personne
            ajouter_avec_photos(nom, solde)
            # Effacer le texte dans la zone
            entree_nom.delete(0, END)
    
    # Bouton "Ajouter une personne"
    btn_ajouter = Button(
        fenetre_admin,
        text="➕ AJOUTER UNE PERSONNE",
        font=("Arial", 11),
        bg="green",
        fg="white",
        width=35,
        command=ajouter_personne
    )
    btn_ajouter.pack(pady=10)
    
    # Fonction pour afficher la liste des personnes
    def afficher_liste():
        # Récupérer la liste des dossiers dans "data"
        liste_personnes = os.listdir("data")
        # Si la liste est vide
        if len(liste_personnes) == 0:
            # Afficher un message
            messagebox.showinfo("Liste", "Aucune personne enregistrée.")
        else:
            # Charger les soldes
            with open("soldes.json", "r") as f:
                soldes = json.load(f)
            # Créer un texte avec toutes les personnes
            texte = "Personnes enregistrées:\n\n"
            for personne in liste_personnes:
                # Afficher le nom et le solde
                solde = soldes.get(personne, "0")
                texte += f"• {personne} (Solde: {solde}€)\n"
            # Afficher le texte
            messagebox.showinfo("Liste des personnes", texte)
    
    # Bouton "Lister les personnes"
    btn_lister = Button(
        fenetre_admin,
        text="📋 LISTER LES PERSONNES",
        font=("Arial", 11),
        bg="blue",
        fg="white",
        width=35,
        command=afficher_liste
    )
    btn_lister.pack(pady=5)
    
    # Fonction pour supprimer une personne
    def supprimer_personne():
        # Récupérer le nom tapé
        nom = entree_nom.get().strip()
        # Vérifier que le nom n'est pas vide
        if nom == "":
            # Afficher une erreur si le nom est vide
            messagebox.showerror("Erreur", "Veuillez entrer un nom!")
        else:
            # Appeler la fonction pour supprimer la personne
            supprimer_avec_photos(nom)
            # Effacer le texte dans la zone
            entree_nom.delete(0, END)
    
    # Bouton "Supprimer une personne"
    btn_supprimer = Button(
        fenetre_admin,
        text="🗑️ SUPPRIMER UNE PERSONNE",
        font=("Arial", 11),
        bg="red",
        fg="white",
        width=35,
        command=supprimer_personne
    )
    btn_supprimer.pack(pady=5)


# ====================================================================
# FONCTION 5 : Ajouter une personne avec photos
# ====================================================================

def ajouter_avec_photos(nom, solde):
    # Créer le chemin du dossier pour cette personne
    chemin_dossier = os.path.join("data", nom)
    
    # Vérifier si la personne existe déjà
    if os.path.exists(chemin_dossier):
        # Afficher une erreur
        messagebox.showerror("Erreur", f"La personne '{nom}' existe déjà!")
        return
    
    # Créer le dossier pour cette personne
    os.makedirs(chemin_dossier)
    
    # Charger les soldes
    with open("soldes.json", "r") as f:
        soldes = json.load(f)
    
    # Ajouter le solde pour cette personne
    soldes[nom] = float(solde)
    
    # Sauvegarder les soldes
    with open("soldes.json", "w") as f:
        json.dump(soldes, f)
    
    # Afficher un message d'information
    messagebox.showinfo(
        "Capture de photos",
        f"Vous allez capturer 10 photos de {nom}.\n"
        f"Appuyez sur SPACE pour capturer une photo.\n"
        f"Appuyez sur ESC pour arrêter."
    )
    
    # Ouvrir la webcam (0 = caméra par défaut)
    capture = cv2.VideoCapture(0)
    
    # Initialiser le compteur de photos à 0
    compteur_photos = 0
    
    # Charger le détecteur de visages (entraîné par OpenCV)
    detecteur_visage = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    # Boucle : continuer tant qu'on n'a pas 10 photos
    while compteur_photos < 10:
        # Lire une image de la webcam
        ret, frame = capture.read()
        
        # Vérifier que la lecture s'est bien passée
        if not ret:
            # Afficher une erreur
            messagebox.showerror("Erreur", "Impossible d'accéder à la webcam!")
            break
        
        # Convertir l'image en niveaux de gris (pour la détection de visages)
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages dans l'image
        visages = detecteur_visage.detectMultiScale(
            frame_gris,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Pour chaque visage détecté
        for (x, y, w, h) in visages:
            # Dessiner un rectangle autour du visage
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Afficher le nombre de photos capturées
        cv2.putText(
            frame,
            f"Photos: {compteur_photos}/10",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        # Afficher la fenêtre avec l'image de la webcam
        cv2.imshow(f"Capture - {nom}", frame)
        
        # Attendre une touche pendant 1 milliseconde
        touche = cv2.waitKey(1) & 0xFF
        
        # Si la touche est SPACE (code 32)
        if touche == 32:
            # Sauvegarder la photo en niveaux de gris
            chemin_photo = os.path.join(chemin_dossier, f"photo_{compteur_photos}.jpg")
            cv2.imwrite(chemin_photo, frame_gris)
            # Augmenter le compteur
            compteur_photos += 1
            # Afficher un message
            messagebox.showinfo("Photo capturée", f"Photo {compteur_photos}/10 capturée!")
        
        # Si la touche est ESC (code 27)
        elif touche == 27:
            # Arrêter la boucle
            break
    
    # Fermer la webcam
    capture.release()
    # Fermer toutes les fenêtres OpenCV
    cv2.destroyAllWindows()
    
    # Afficher un message de succès
    messagebox.showinfo("Succès", f"{compteur_photos} photos capturées pour {nom}!")


# ====================================================================
# FONCTION 6 : Supprimer une personne
# ====================================================================

def supprimer_avec_photos(nom):
    # Créer le chemin du dossier
    chemin_dossier = os.path.join("data", nom)
    
    # Vérifier si la personne existe
    if not os.path.exists(chemin_dossier):
        # Afficher une erreur
        messagebox.showerror("Erreur", f"La personne '{nom}' n'existe pas!")
        return
    
    # Demander une confirmation
    reponse = messagebox.askyesno(
        "Confirmation",
        f"Êtes-vous sûr de vouloir supprimer '{nom}' ?"
    )
    
    # Si la réponse est "Oui"
    if reponse:
        # Importer shutil pour supprimer un dossier
        import shutil
        # Supprimer le dossier et tout son contenu
        shutil.rmtree(chemin_dossier)
        
        # Charger les soldes
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
        
        # Supprimer le solde de cette personne
        if nom in soldes:
            del soldes[nom]
        
        # Sauvegarder les soldes
        with open("soldes.json", "w") as f:
            json.dump(soldes, f)
        
        # Afficher un message de succès
        messagebox.showinfo("Succès", f"'{nom}' a été supprimée!")


# ====================================================================
# FONCTION 6 : Entraîner le modèle de reconnaissance
# ====================================================================

def entrainer_modele():
    # Créer deux listes vides
    # Une pour les images, une pour les noms
    images = []
    noms = []
    
    # Parcourir chaque dossier dans "data"
    for nom_personne in os.listdir("data"):
        # Créer le chemin complet du dossier
        chemin_dossier = os.path.join("data", nom_personne)
        
        # Vérifier que c'est un dossier (pas un fichier)
        if not os.path.isdir(chemin_dossier):
            continue
        
        # Parcourir chaque photo dans le dossier
        for nom_photo in os.listdir(chemin_dossier):
            # Créer le chemin complet de la photo
            chemin_photo = os.path.join(chemin_dossier, nom_photo)
            
            # Charger l'image en niveaux de gris
            image = cv2.imread(chemin_photo, 0)
            
            # Vérifier que l'image s'est bien chargée
            if image is None:
                continue
            
            # Ajouter l'image à la liste
            images.append(image)
            # Ajouter le nom à la liste
            noms.append(nom_personne)
    
    # Vérifier qu'il y a au moins une image
    if len(images) == 0:
        # Afficher une erreur
        messagebox.showerror(
            "Erreur",
            "Aucune photo trouvée! Ajoutez d'abord des personnes."
        )
        return
    
    # Créer un reconnaisseur LBPH (algorithme de reconnaissance faciale)
    reconnaisseur = cv2.face.LBPHFaceRecognizer_create()
    
    # Entraîner le modèle avec les images et les noms
    reconnaisseur.train(images, np.array([hash(nom) % 100 for nom in noms]))
    
    # Sauvegarder le modèle dans un fichier
    reconnaisseur.save("modele_reconnaissance.yml")
    
    # Créer un dictionnaire pour mapper les noms aux numéros
    label_map = {}
    for i, nom in enumerate(set(noms)):
        label_map[hash(nom) % 100] = nom
    
    # Sauvegarder le mappage dans un fichier
    import json
    with open("label_map.json", "w") as f:
        json.dump(label_map, f)
    
    # Afficher un message de succès
    messagebox.showinfo("Succès", "Modèle entraîné avec succès!")


# ====================================================================
# FONCTION 9 : Interface Identification
# ====================================================================

def interface_identification():
    # Afficher un message d'information
    messagebox.showinfo(
        "Identification",
        "Regardez la webcam.\n"
        f"Appuyez sur ESC pour arrêter."
    )
    
    # Charger le modèle entraîné
    reconnaisseur = cv2.face.LBPHFaceRecognizer_create()
    
    # Vérifier que le modèle existe
    if not os.path.exists("modele_reconnaissance.yml"):
        # Afficher une erreur
        messagebox.showerror(
            "Erreur",
            "Le modèle n'existe pas!\n"
            "Allez en mode Administrateur pour ajouter des personnes d'abord."
        )
        return
    
    # Charger le modèle
    reconnaisseur.read("modele_reconnaissance.yml")
    
    # Charger le mappage
    import json
    with open("label_map.json", "r") as f:
        label_map = json.load(f)
    
    # Charger les soldes
    with open("soldes.json", "r") as f:
        soldes = json.load(f)
    
    # Ouvrir la webcam
    capture = cv2.VideoCapture(0)
    
    # Charger le détecteur de visages
    detecteur_visage = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    # Booléen pour vérifier si déjà identifié
    identifie = False
    
    # Boucle d'identification
    while not identifie:
        # Lire une image de la webcam
        ret, frame = capture.read()
        
        # Vérifier que la lecture s'est bien passée
        if not ret:
            # Afficher une erreur
            messagebox.showerror("Erreur", "Impossible d'accéder à la webcam!")
            break
        
        # Convertir en niveaux de gris
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages
        visages = detecteur_visage.detectMultiScale(
            frame_gris,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Pour chaque visage détecté
        for (x, y, w, h) in visages:
            # Extraire le visage
            visage = frame_gris[y:y + h, x:x + w]
            
            # Identifier le visage
            label, confiance = reconnaisseur.predict(visage)
            
            # Si confiance < 100, c'est un visage reconnu
            if confiance < 100:
                # Récupérer le nom du visage
                nom = label_map.get(str(label), "Inconnu")
                
                # Récupérer le solde
                solde_actuel = soldes.get(nom, 0)
                
                # Vérifier que le solde est suffisant (5€ pour un repas)
                if solde_actuel >= 5:
                    # Déduire 5€ du solde
                    soldes[nom] = solde_actuel - 5
                    
                    # Sauvegarder les soldes
                    with open("soldes.json", "w") as f:
                        json.dump(soldes, f)
                    
                    # Afficher un message de succès
                    messagebox.showinfo(
                        "Succès",
                        f"Bienvenue {nom}!\n"
                        f"Repas crédité!\n"
                        f"Ancien solde: {solde_actuel:.2f}€\n"
                        f"Nouveau solde: {soldes[nom]:.2f}€"
                    )
                else:
                    # Afficher un message d'erreur (solde insuffisant)
                    messagebox.showerror(
                        "Erreur",
                        f"{nom},\n"
                        f"Solde insuffisant!\n"
                        f"Solde actuel: {solde_actuel:.2f}€"
                    )
                
                # Arrêter la boucle
                identifie = True
                break
            
            # Dessiner un rectangle autour du visage
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Afficher la confiance
            cv2.putText(
                frame,
                f"Confiance: {confiance:.0f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
        
        # Afficher la fenêtre
        cv2.imshow("Identification", frame)
        
        # Attendre une touche
        touche = cv2.waitKey(1) & 0xFF
        # Si ESC est appuyé
        if touche == 27:
            # Arrêter la boucle
            break
    
    # Fermer la webcam
    capture.release()
    # Fermer toutes les fenêtres OpenCV
    cv2.destroyAllWindows()


# ====================================================================
# POINT D'ENTRÉE - LANCER L'APPLICATION
# ====================================================================

# Vérifier que le fichier est exécuté directement
if __name__ == "__main__":
    # Créer les dossiers nécessaires
    creer_dossiers()
    # Créer le fichier des soldes
    creer_fichier_soldes()
    # Lancer l'interface principale
    interface_principale()
