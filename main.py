# ====================================================================
# APPLICATION RECONNAISSANCE FACIALE - RESTAURANT SCOLAIRE
# ====================================================================

# Importer OpenCV pour la webcam et la reconnaissance faciale
import cv2
# Importer os pour créer/gérer des dossiers
import os
# Importer numpy pour les calculs mathématiques
import numpy as np
# Importer tkinter pour faire l'interface graphique
from tkinter import *
# Importer messagebox pour afficher des messages
from tkinter import messagebox
# Importer PIL pour afficher des images
from PIL import Image, ImageTk
# Importer json pour sauvegarder les soldes
import json
# Importer threading pour les traitements en arrière-plan
import threading


# ====================================================================
# VARIABLES GLOBALES
# ====================================================================

# Fenêtre principale unique
fenetre_principale = None
# Cadre principal (frame)
frame_principal = None
# Webcam
capture_webcam = None
# Booléen pour arrêter la webcam
arreter_webcam = False


# ====================================================================
# FONCTION : Créer les dossiers et fichiers
# ====================================================================

def creer_dossiers_fichiers():
    # Créer le dossier "data" s'il n'existe pas
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Créer le fichier des soldes s'il n'existe pas
    if not os.path.exists("soldes.json"):
        with open("soldes.json", "w") as f:
            json.dump({}, f)


# ====================================================================
# FONCTION : Afficher le menu principal
# ====================================================================

def afficher_menu_principal():
    # Détruire tous les widgets du frame
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Arrêter la webcam si active
    global arreter_webcam
    arreter_webcam = True
    
    # Titre
    titre = Label(
        frame_principal,
        text="RESTAURANT SCOLAIRE",
        font=("Arial", 20, "bold"),
        bg="lightblue"
    )
    titre.pack(pady=20)
    
    # Sous-titre
    sous_titre = Label(
        frame_principal,
        text="Choisissez une option:",
        font=("Arial", 14),
        bg="lightblue"
    )
    sous_titre.pack(pady=10)
    
    # Bouton Administrateur
    btn_admin = Button(
        frame_principal,
        text="👤 ADMINISTRATEUR",
        font=("Arial", 12, "bold"),
        bg="orange",
        fg="white",
        width=30,
        command=afficher_login_admin
    )
    btn_admin.pack(pady=15)
    
    # Bouton M'identifier
    btn_identifier = Button(
        frame_principal,
        text="✓ M'IDENTIFIER",
        font=("Arial", 12, "bold"),
        bg="green",
        fg="white",
        width=30,
        command=afficher_identification
    )
    btn_identifier.pack(pady=15)


# ====================================================================
# FONCTION : Afficher le login administrateur
# ====================================================================

def afficher_login_admin():
    # Détruire tous les widgets du frame
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Titre
    titre = Label(
        frame_principal,
        text="CONNEXION ADMINISTRATEUR",
        font=("Arial", 16, "bold"),
        bg="lightyellow"
    )
    titre.pack(pady=10)
    
    # Label Identifiant
    label_id = Label(
        frame_principal,
        text="Identifiant:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_id.pack(pady=5)
    
    # Entry Identifiant
    entree_id = Entry(frame_principal, font=("Arial", 11), width=30)
    entree_id.pack(pady=5)
    
    # Label Mot de passe
    label_pass = Label(
        frame_principal,
        text="Mot de passe:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_pass.pack(pady=5)
    
    # Entry Mot de passe
    entree_pass = Entry(frame_principal, font=("Arial", 11), width=30, show="*")
    entree_pass.pack(pady=5)
    
    # Fonction pour vérifier
    def verifier():
        # Récupérer les valeurs
        id_admin = entree_id.get()
        pass_admin = entree_pass.get()
        
        # Vérifier
        if id_admin == "admin" and pass_admin == "admin":
            # Aller à l'interface admin
            afficher_menu_admin()
        else:
            # Afficher une erreur
            messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect!")
    
    # Bouton Connexion
    btn_connexion = Button(
        frame_principal,
        text="Connexion",
        font=("Arial", 11),
        bg="orange",
        fg="white",
        width=20,
        command=verifier
    )
    btn_connexion.pack(pady=10)
    
    # Bouton Retour
    btn_retour = Button(
        frame_principal,
        text="← RETOUR",
        font=("Arial", 11),
        bg="gray",
        fg="white",
        width=20,
        command=afficher_menu_principal
    )
    btn_retour.pack(pady=10)


# ====================================================================
# FONCTION : Afficher le menu administrateur
# ====================================================================

def afficher_menu_admin():
    # Détruire tous les widgets du frame
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Titre
    titre = Label(
        frame_principal,
        text="INTERFACE ADMINISTRATEUR",
        font=("Arial", 14, "bold"),
        bg="lightyellow"
    )
    titre.pack(pady=10)
    
    # Label Nom
    label_nom = Label(
        frame_principal,
        text="Nom de la personne:",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_nom.pack(pady=5)
    
    # Entry Nom
    entree_nom = Entry(frame_principal, font=("Arial", 11), width=30)
    entree_nom.pack(pady=5)
    
    # Label Solde
    label_solde = Label(
        frame_principal,
        text="Solde initial (€):",
        font=("Arial", 11),
        bg="lightyellow"
    )
    label_solde.pack(pady=5)
    
    # Entry Solde
    entree_solde = Entry(frame_principal, font=("Arial", 11), width=30)
    entree_solde.insert(0, "50")
    entree_solde.pack(pady=5)
    
    # Fonction pour ajouter
    def ajouter():
        nom = entree_nom.get().strip()
        solde = entree_solde.get().strip()
        
        if nom == "":
            messagebox.showerror("Erreur", "Veuillez entrer un nom!")
        else:
            try:
                solde = float(solde)
                # Aller à la capture de photos
                afficher_capture_photos(nom, solde)
            except:
                messagebox.showerror("Erreur", "Le solde doit être un nombre!")
    
    # Bouton Ajouter
    btn_ajouter = Button(
        frame_principal,
        text="➕ AJOUTER UNE PERSONNE",
        font=("Arial", 11),
        bg="green",
        fg="white",
        width=35,
        command=ajouter
    )
    btn_ajouter.pack(pady=10)
    
    # Fonction pour afficher la liste
    def afficher_liste():
        liste_personnes = os.listdir("data")
        
        if len(liste_personnes) == 0:
            messagebox.showinfo("Liste", "Aucune personne enregistrée.")
        else:
            with open("soldes.json", "r") as f:
                soldes = json.load(f)
            
            texte = "Personnes enregistrées:\n\n"
            for personne in liste_personnes:
                solde = soldes.get(personne, "0")
                texte += f"• {personne} (Solde: {solde}€)\n"
            
            messagebox.showinfo("Liste des personnes", texte)
    
    # Bouton Lister
    btn_lister = Button(
        frame_principal,
        text="📋 LISTER LES PERSONNES",
        font=("Arial", 11),
        bg="blue",
        fg="white",
        width=35,
        command=afficher_liste
    )
    btn_lister.pack(pady=5)
    
    # Fonction pour supprimer
    def supprimer():
        nom = entree_nom.get().strip()
        
        if nom == "":
            messagebox.showerror("Erreur", "Veuillez entrer un nom!")
        else:
            chemin_dossier = os.path.join("data", nom)
            
            if not os.path.exists(chemin_dossier):
                messagebox.showerror("Erreur", f"La personne '{nom}' n'existe pas!")
            else:
                reponse = messagebox.askyesno(
                    "Confirmation",
                    f"Êtes-vous sûr de vouloir supprimer '{nom}'?"
                )
                
                if reponse:
                    import shutil
                    shutil.rmtree(chemin_dossier)
                    
                    with open("soldes.json", "r") as f:
                        soldes = json.load(f)
                    
                    if nom in soldes:
                        del soldes[nom]
                    
                    with open("soldes.json", "w") as f:
                        json.dump(soldes, f)
                    
                    messagebox.showinfo("Succès", f"'{nom}' a été supprimée!")
                    entree_nom.delete(0, END)
    
    # Bouton Supprimer
    btn_supprimer = Button(
        frame_principal,
        text="🗑️ SUPPRIMER UNE PERSONNE",
        font=("Arial", 11),
        bg="red",
        fg="white",
        width=35,
        command=supprimer
    )
    btn_supprimer.pack(pady=5)
    
    # Bouton Retour
    btn_retour = Button(
        frame_principal,
        text="← RETOUR",
        font=("Arial", 11),
        bg="gray",
        fg="white",
        width=35,
        command=afficher_menu_principal
    )
    btn_retour.pack(pady=10)


# ====================================================================
# FONCTION : Afficher la capture de photos
# ====================================================================

def afficher_capture_photos(nom, solde):
    # Détruire tous les widgets du frame
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Créer le dossier
    chemin_dossier = os.path.join("data", nom)
    
    if os.path.exists(chemin_dossier):
        messagebox.showerror("Erreur", f"La personne '{nom}' existe déjà!")
        afficher_menu_admin()
        return
    
    os.makedirs(chemin_dossier)
    
    # Sauvegarder le solde
    with open("soldes.json", "r") as f:
        soldes_dict = json.load(f)
    
    soldes_dict[nom] = solde
    
    with open("soldes.json", "w") as f:
        json.dump(soldes_dict, f)
    
    # Titre
    titre = Label(
        frame_principal,
        text=f"CAPTURE DE PHOTOS - {nom}",
        font=("Arial", 14, "bold"),
        bg="lightyellow"
    )
    titre.pack(pady=10)
    
    # Label du statut
    label_statut = Label(
        frame_principal,
        text="Montrez votre visage à la webcam...",
        font=("Arial", 12),
        bg="lightyellow"
    )
    label_statut.pack(pady=10)
    
    # Canvas pour afficher la webcam
    canvas = Canvas(frame_principal, width=400, height=300, bg="black")
    canvas.pack(pady=10)
    
    # Variables
    compteur_photos = [0]  # Utiliser une liste pour pouvoir modifier dans la fonction
    
    # Fonction pour capturer
    def capturer_photos():
        global capture_webcam, arreter_webcam
        
        # Ouvrir la webcam
        capture_webcam = cv2.VideoCapture(0)
        arreter_webcam = False
        
        # Charger le détecteur de visages
        detecteur_visage = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        
        # Boucle de capture
        while compteur_photos[0] < 10 and not arreter_webcam:
            ret, frame = capture_webcam.read()
            
            if not ret:
                break
            
            # Convertir en niveaux de gris pour la détection
            frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Détecter les visages
            visages = detecteur_visage.detectMultiScale(
                frame_gris,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Redimensionner pour l'affichage
            frame_petit = cv2.resize(frame, (400, 300))
            
            # Redimensionner aussi les coordonnées des visages
            echelle = 300 / frame.shape[0]
            
            # Dessiner les rectangles autour des visages
            for (x, y, w, h) in visages:
                x_petit = int(x * echelle)
                y_petit = int(y * echelle)
                w_petit = int(w * echelle)
                h_petit = int(h * echelle)
                # Dessiner un rectangle vert
                cv2.rectangle(frame_petit, (x_petit, y_petit), (x_petit + w_petit, y_petit + h_petit), (0, 255, 0), 2)
            
            # Si un visage est détecté
            if len(visages) > 0:
                # Sauvegarder la photo
                chemin_photo = os.path.join(chemin_dossier, f"photo_{compteur_photos[0]}.jpg")
                cv2.imwrite(chemin_photo, frame_gris)
                compteur_photos[0] += 1
                
                # Attendre un peu avant la prochaine capture (pour diversifier)
                import time
                time.sleep(0.5)
            
            # Convertir pour Tkinter
            frame_rgb = cv2.cvtColor(frame_petit, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(img)
            
            canvas.create_image(0, 0, image=photo, anchor=NW)
            canvas.image = photo
            
            # Mettre à jour le statut
            label_statut.config(text=f"Photos capturées: {compteur_photos[0]}/10")
            frame_principal.update()
        
        # Fermer la webcam
        if capture_webcam:
            capture_webcam.release()
        
        # Vider le canvas
        canvas.delete("all")
        
        # Afficher le résultat
        label_statut.config(text=f"Capture terminée! {compteur_photos[0]} photos capturées.")
    
    # Démarrer la capture dans un thread
    thread_capture = threading.Thread(target=capturer_photos)
    thread_capture.start()
    
    # Fonction pour arrêter
    def arreter():
        global arreter_webcam
        arreter_webcam = True
        thread_capture.join()
        afficher_menu_admin()
    
    # Bouton Arrêter
    btn_arreter = Button(
        frame_principal,
        text="⏹️ ARRÊTER",
        font=("Arial", 11),
        bg="red",
        fg="white",
        width=20,
        command=arreter
    )
    btn_arreter.pack(pady=10)


# ====================================================================
# FONCTION : Afficher l'identification
# ====================================================================

def afficher_identification():
    # Détruire tous les widgets du frame
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Vérifier qu'il y a des personnes
    liste_personnes = os.listdir("data")
    
    if len(liste_personnes) == 0:
        messagebox.showerror(
            "Erreur",
            "Aucune personne enregistrée!\n"
            "Allez en mode Administrateur pour ajouter des personnes."
        )
        afficher_menu_principal()
        return
    
    # Titre
    titre = Label(
        frame_principal,
        text="IDENTIFICATION",
        font=("Arial", 14, "bold"),
        bg="lightgreen"
    )
    titre.pack(pady=10)
    
    # Label du statut
    label_statut = Label(
        frame_principal,
        text="Montrez votre visage à la webcam...",
        font=("Arial", 12),
        bg="lightgreen"
    )
    label_statut.pack(pady=10)
    
    # Canvas pour afficher la webcam
    canvas = Canvas(frame_principal, width=400, height=300, bg="black")
    canvas.pack(pady=10)
    
    # Variable pour stocker si identifié
    identifie = [False]
    
    # Fonction pour identifier
    def identifier():
        global capture_webcam, arreter_webcam
        
        # Ouvrir la webcam
        capture_webcam = cv2.VideoCapture(0)
        arreter_webcam = False
        
        # Charger le détecteur de visages
        detecteur_visage = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        
        # Charger le reconnaisseur
        reconnaisseur = cv2.face.LBPHFaceRecognizer_create()
        
        # Vérifier que le modèle existe
        if not os.path.exists("modele_reconnaissance.yml"):
            # Entraîner le modèle
            images = []
            noms = []
            
            for nom_personne in liste_personnes:
                chemin_dossier = os.path.join("data", nom_personne)
                
                for nom_photo in os.listdir(chemin_dossier):
                    chemin_photo = os.path.join(chemin_dossier, nom_photo)
                    image = cv2.imread(chemin_photo, 0)
                    
                    if image is not None:
                        images.append(image)
                        noms.append(nom_personne)
            
            if len(images) > 0:
                # Créer les labels
                labels_uniques = {}
                label_id = 0
                for nom in noms:
                    if nom not in labels_uniques:
                        labels_uniques[nom] = label_id
                        label_id += 1
                
                # Créer les arrays
                images_array = np.array(images)
                labels_array = np.array([labels_uniques[nom] for nom in noms])
                
                # Entraîner
                reconnaisseur.train(images_array, labels_array)
                reconnaisseur.save("modele_reconnaissance.yml")
                
                # Sauvegarder le mappage
                label_map = {v: k for k, v in labels_uniques.items()}
                
                with open("label_map.json", "w") as f:
                    json.dump(label_map, f)
        
        # Charger le modèle
        reconnaisseur.read("modele_reconnaissance.yml")
        
        # Charger le mappage
        with open("label_map.json", "r") as f:
            label_map = json.load(f)
        
        # Charger les soldes
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
        
        # Boucle d'identification
        while not identifie[0] and not arreter_webcam:
            ret, frame = capture_webcam.read()
            
            if not ret:
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
            
            # Redimensionner pour l'affichage
            frame_petit = cv2.resize(frame, (400, 300))
            echelle = 300 / frame.shape[0]
            
            # Pour chaque visage détecté
            for (x, y, w, h) in visages:
                # Extraire le visage
                visage = frame_gris[y:y + h, x:x + w]
                
                # Identifier
                label, confiance = reconnaisseur.predict(visage)
                
                # Afficher le rectangle
                x_petit = int(x * echelle)
                y_petit = int(y * echelle)
                w_petit = int(w * echelle)
                h_petit = int(h * echelle)
                
                # Si reconnu (confiance < 100)
                if confiance < 100:
                    # Dessiner en vert
                    cv2.rectangle(frame_petit, (x_petit, y_petit), (x_petit + w_petit, y_petit + h_petit), (0, 255, 0), 2)
                    
                    # Récupérer le nom
                    nom = label_map.get(str(label), "Inconnu")
                    
                    # Récupérer le solde
                    solde_actuel = soldes.get(nom, 0)
                    
                    # Vérifier le solde
                    if solde_actuel >= 5:
                        # Débiter 5€
                        soldes[nom] = solde_actuel - 5
                        
                        with open("soldes.json", "w") as f:
                            json.dump(soldes, f)
                        
                        # Afficher le succès
                        label_statut.config(
                            text=f"✓ Bienvenue {nom}!\nRepas crédité!\nAncien: {solde_actuel:.2f}€ → Nouveau: {soldes[nom]:.2f}€",
                            fg="green"
                        )
                        identifie[0] = True
                    else:
                        # Solde insuffisant
                        label_statut.config(
                            text=f"✗ {nom}\nSolde insuffisant: {solde_actuel:.2f}€",
                            fg="red"
                        )
                        identifie[0] = True
                    
                    break
                else:
                    # Dessiner en rouge (pas reconnu)
                    cv2.rectangle(frame_petit, (x_petit, y_petit), (x_petit + w_petit, y_petit + h_petit), (0, 0, 255), 2)
            
            # Afficher le frame
            frame_rgb = cv2.cvtColor(frame_petit, cv2.COLOR_BGR2RGB)
            
            img = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(img)
            
            canvas.create_image(0, 0, image=photo, anchor=NW)
            canvas.image = photo
            
            frame_principal.update()
        
        # Fermer la webcam
        if capture_webcam:
            capture_webcam.release()
    
    # Démarrer l'identification dans un thread
    thread_id = threading.Thread(target=identifier)
    thread_id.start()
    
    # Fonction pour arrêter
    def arreter():
        global arreter_webcam
        arreter_webcam = True
        thread_id.join()
        afficher_menu_principal()
    
    # Bouton Retour
    btn_retour = Button(
        frame_principal,
        text="← RETOUR",
        font=("Arial", 11),
        bg="gray",
        fg="white",
        width=20,
        command=arreter
    )
    btn_retour.pack(pady=10)


# ====================================================================
# POINT D'ENTRÉE
# ====================================================================

if __name__ == "__main__":
    # Créer les dossiers et fichiers
    creer_dossiers_fichiers()
    
    # Créer la fenêtre principale
    fenetre_principale = Tk()
    fenetre_principale.title("Restaurant - Reconnaissance Faciale")
    fenetre_principale.geometry("600x500")
    fenetre_principale.configure(bg="lightblue")
    
    # Créer le frame principal
    frame_principal = Frame(fenetre_principale, bg="lightblue")
    frame_principal.pack(fill=BOTH, expand=True)
    
    # Afficher le menu principal
    afficher_menu_principal()
    
    # Lancer la fenêtre
    fenetre_principale.mainloop()
