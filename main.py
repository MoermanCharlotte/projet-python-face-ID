# ====================================================================
# APPLICATION SIMPLE - RECONNAISSANCE FACIALE
# ====================================================================
# Cette application permet aux utilisateurs de:
# 1. S'identifier via reconnaissance faciale
# 2. Débiter leur solde (5€ par repas)
# Les administrateurs peuvent ajouter/supprimer des personnes
# ====================================================================

# Importer les librairies nécessaires
import cv2           # Pour la webcam et la reconnaissance faciale
import os            # Pour gérer les dossiers
import numpy as np   # Pour les tableaux
from tkinter import *       # Pour l'interface graphique
from tkinter import messagebox  # Pour les popups
import json          # Pour stocker les données

# Variables globales pour stocker les éléments de l'interface
fenetre = None           # La fenêtre principale
frame_principal = None   # Le cadre principal qui change selon la page

# ====================================================================
# CRÉER LES DOSSIERS ET FICHIERS NÉCESSAIRES
# ====================================================================
# Créer le dossier "data" s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

# Créer le fichier "soldes.json" s'il n'existe pas
# Ce fichier stocke l'argent de chaque personne (ex: {"Alice": 50.0, "Bob": 30.0})
if not os.path.exists("soldes.json"):
    with open("soldes.json", "w") as f:
        json.dump({}, f)

# ====================================================================
# MENU PRINCIPAL - Première page quand on lance l'app
# ====================================================================
def menu_principal():
    """
    Affiche le menu principal avec deux choix:
    - ADMINISTRATEUR (pour ajouter/supprimer des personnes)
    - M'IDENTIFIER (pour se reconnaître)
    """
    
    # Vider le frame (supprimer tous les widgets de l'écran précédent)
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Afficher le titre
    Label(frame_principal, text="RESTAURANT", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)
    
    # Bouton pour se connecter en tant qu'administrateur
    Button(frame_principal, text="ADMINISTRATEUR", font=("Arial", 14), bg="orange", fg="white", width=25, command=login_admin).pack(pady=10)
    
    # Bouton pour s'identifier avec la reconnaissance faciale
    Button(frame_principal, text="M'IDENTIFIER", font=("Arial", 14), bg="green", fg="white", width=25, command=mode_identification).pack(pady=10)

# ====================================================================
# LOGIN ADMINISTRATEUR - Demander le mot de passe
# ====================================================================
def login_admin():
    """
    Affiche l'écran de connexion pour l'administrateur
    Les identifiants par défaut sont: admin / admin
    """
    
    # Vider l'écran précédent
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Titre de la page
    Label(frame_principal, text="LOGIN ADMIN", font=("Arial", 16, "bold"), bg="lightyellow").pack(pady=10)
    
    # Champ pour l'ID
    Label(frame_principal, text="ID:", font=("Arial", 12), bg="lightyellow").pack()
    entry_id = Entry(frame_principal, font=("Arial", 12), width=25)
    entry_id.pack(pady=5)
    
    # Champ pour le mot de passe
    Label(frame_principal, text="PASSWORD:", font=("Arial", 12), bg="lightyellow").pack()
    entry_pass = Entry(frame_principal, font=("Arial", 12), width=25, show="*")
    entry_pass.pack(pady=5)
    
    def verifier():
        """Vérifier les identifiants"""
        # Si ID = "admin" ET mot de passe = "admin", on passe au menu admin
        if entry_id.get() == "admin" and entry_pass.get() == "admin":
            menu_admin()
        else:
            # Sinon afficher une erreur
            messagebox.showerror("Erreur", "Incorrect!")
    
    # Bouton pour se connecter
    Button(frame_principal, text="Connexion", font=("Arial", 12), bg="orange", fg="white", command=verifier).pack(pady=10)
    
    # Bouton pour revenir au menu principal
    Button(frame_principal, text="Retour", font=("Arial", 12), bg="gray", fg="white", command=menu_principal).pack(pady=5)

# ====================================================================
# MENU ADMINISTRATEUR - Ajouter/Lister/Supprimer des personnes
# ====================================================================
def menu_admin():
    """
    Affiche le menu d'administration avec options pour:
    - AJOUTER une nouvelle personne (capture 10 photos)
    - LISTER toutes les personnes
    - SUPPRIMER une personne
    """
    
    # Vider l'écran
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Titre
    Label(frame_principal, text="ADMINISTRATEUR", font=("Arial", 16, "bold"), bg="lightyellow").pack(pady=10)
    
    # Champ pour entrer le nom
    Label(frame_principal, text="Nom:", font=("Arial", 12), bg="lightyellow").pack()
    entry_nom = Entry(frame_principal, font=("Arial", 12), width=25)
    entry_nom.pack(pady=5)
    
    # Champ pour entrer le solde (argent initial)
    Label(frame_principal, text="Solde:", font=("Arial", 12), bg="lightyellow").pack()
    entry_solde = Entry(frame_principal, font=("Arial", 12), width=25)
    entry_solde.insert(0, "50")  # Par défaut 50€
    entry_solde.pack(pady=5)
    
    def ajouter():
        """Ajouter une nouvelle personne"""
        nom = entry_nom.get().strip()
        solde = entry_solde.get().strip()
        
        # Vérifier que le nom n'est pas vide
        if not nom:
            messagebox.showerror("Erreur", "Nom vide!")
            return
        
        # Vérifier que le solde est un nombre valide
        try:
            solde = float(solde)
        except:
            messagebox.showerror("Erreur", "Solde invalide!")
            return
        
        # Vérifier que la personne n'existe pas déjà
        chemin = os.path.join("data", nom)
        if os.path.exists(chemin):
            messagebox.showerror("Erreur", "Personne existe déjà!")
            return
        
        # Créer le dossier pour stocker les photos
        os.makedirs(chemin)
        
        # Sauvegarder le solde dans le fichier JSON
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
        soldes[nom] = solde
        with open("soldes.json", "w") as f:
            json.dump(soldes, f)
        
        # Capturer les 10 photos de la personne
        capturer(nom, chemin)
    
    def lister():
        """Afficher la liste de toutes les personnes"""
        personnes = os.listdir("data")
        if not personnes:
            messagebox.showinfo("Liste", "Aucun")
            return
        
        # Charger les soldes
        with open("soldes.json", "r") as f:
            soldes = json.load(f)
        
        # Construire le texte à afficher
        texte = "Personnes:\n\n"
        for p in personnes:
            texte += f"{p} - Solde: {soldes.get(p, 0)}€\n"
        
        messagebox.showinfo("Liste", texte)
    
    def supprimer():
        """Supprimer une personne"""
        nom = entry_nom.get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Nom vide!")
            return
        
        chemin = os.path.join("data", nom)
        if not os.path.exists(chemin):
            messagebox.showerror("Erreur", "Pas trouvé!")
            return
        
        # Demander confirmation
        if messagebox.askyesno("Confirmation", f"Supprimer {nom}?"):
            # Supprimer le dossier
            import shutil
            shutil.rmtree(chemin)
            
            # Supprimer du fichier soldes.json
            with open("soldes.json", "r") as f:
                soldes = json.load(f)
            if nom in soldes:
                del soldes[nom]
            with open("soldes.json", "w") as f:
                json.dump(soldes, f)
            
            messagebox.showinfo("Succès", "Supprimé!")
    
    # Boutons d'action
    Button(frame_principal, text="AJOUTER", font=("Arial", 12), bg="green", fg="white", width=25, command=ajouter).pack(pady=5)
    Button(frame_principal, text="LISTER", font=("Arial", 12), bg="blue", fg="white", width=25, command=lister).pack(pady=5)
    Button(frame_principal, text="SUPPRIMER", font=("Arial", 12), bg="red", fg="white", width=25, command=supprimer).pack(pady=5)
    Button(frame_principal, text="Retour", font=("Arial", 12), bg="gray", fg="white", width=25, command=menu_principal).pack(pady=10)

# ====================================================================
# CAPTURER LES PHOTOS - Prendre 10 photos pour la reconnaissance faciale
# ====================================================================
def capturer(nom, chemin):
    """
    Capture 10 photos de la personne pour la reconnaissance faciale.
    
    Instructions:
    - Appuyez sur SPACE pour prendre une photo (quand un visage est détecté)
    - Appuyez sur ESC pour arrêter
    - Les photos seront sauvegardées en niveaux de gris
    
    Paramètres:
    - nom: le nom de la personne
    - chemin: le dossier où sauvegarder les photos
    """
    
    messagebox.showinfo("Capture", "Cliquez OK puis montrez votre visage")
    
    # Ouvrir la webcam (0 = caméra par défaut)
    cap = cv2.VideoCapture(0)
    
    # Charger le détecteur de visage (algorithme Haar Cascade)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    compteur = 0  # Compteur des photos prises
    
    # Boucle: continuer jusqu'à 10 photos
    while compteur < 10:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir l'image en niveaux de gris (obligatoire pour la reconnaissance)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages dans l'image
        # (1.3 = facteur d'échelle, 5 = nombre minimum de voisins)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        # Dessiner un rectangle vert autour de chaque visage détecté
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Afficher le compteur sur l'écran
        cv2.putText(frame, f"Photos: {compteur}/10", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Afficher la fenêtre avec le flux vidéo
        cv2.imshow(f"Capture - {nom}", frame)
        
        # Attendre une touche clavier
        key = cv2.waitKey(1) & 0xFF
        
        # SPACE = capturer une photo
        if key == 32 and len(faces) > 0:
            # Sauvegarder l'image en niveaux de gris
            chemin_photo = os.path.join(chemin, f"photo_{compteur}.jpg")
            cv2.imwrite(chemin_photo, gray)
            compteur += 1
        
        # ESC = arrêter la capture
        elif key == 27:
            break
    
    # Libérer la caméra
    cap.release()
    # Fermer les fenêtres OpenCV
    cv2.destroyAllWindows()
    
    messagebox.showinfo("Succès", f"{compteur} photos capturées!")

# ====================================================================
# IDENTIFICATION - Reconnaître une personne et débiter son solde
# ====================================================================
def mode_identification():
    """
    Mode identification par reconnaissance faciale.
    
    Processus:
    1. Charger toutes les photos enregistrées
    2. Entraîner le modèle LBPH
    3. Afficher le flux vidéo avec détection de visages
    4. L'utilisateur clique sur "IDENTIFIER" quand son visage est bien détecté
    5. Débiter 5€ de son solde
    """
    
    # Vérifier qu'il y a des personnes enregistrées
    personnes = os.listdir("data")
    if not personnes:
        messagebox.showerror("Erreur", "Aucune personne enregistrée!")
        menu_principal()
        return
    
    # Vider l'écran
    for widget in frame_principal.winfo_children():
        widget.destroy()
    
    # Titre
    Label(frame_principal, text="IDENTIFICATION", font=("Arial", 16, "bold"), bg="lightgreen").pack(pady=10)
    Label(frame_principal, text="Montrez votre visage à la caméra", font=("Arial", 12), bg="lightgreen").pack(pady=5)
    
    # ==============================================================
    # ÉTAPE 1: Charger toutes les photos et entraîner le modèle
    # ==============================================================
    
    images = []      # Liste de toutes les images
    labels_list = [] # Liste des labels correspondants
    label_map = {}   # Dictionnaire pour mapper label ID → nom personne
    label_id = 0     # Compteur pour les IDs de label
    
    # Pour chaque personne enregistrée
    for nom_personne in personnes:
        chemin_dossier = os.path.join("data", nom_personne)
        label_map[label_id] = nom_personne  # Mapper l'ID au nom
        
        # Pour chaque photo de la personne
        for nom_photo in os.listdir(chemin_dossier):
            chemin_photo = os.path.join(chemin_dossier, nom_photo)
            # Charger l'image en niveaux de gris
            image = cv2.imread(chemin_photo, 0)
            if image is not None:
                images.append(image)
                labels_list.append(label_id)
        
        label_id += 1
    
    # Vérifier qu'il y a des images
    if not images:
        messagebox.showerror("Erreur", "Pas de photos!")
        menu_principal()
        return
    
    # Créer et entraîner le modèle LBPH
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, np.array(labels_list))
    
    print(f"Modèle entraîné avec {len(images)} images, {len(label_map)} personnes")
    print(f"Mapping: {label_map}")
    
    # ==============================================================
    # ÉTAPE 2: Afficher le flux vidéo avec détection de visages
    # ==============================================================
    
    # Variables pour stocker le flux vidéo
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Charger les soldes
    with open("soldes.json", "r") as f:
        soldes = json.load(f)
    
    # Variables pour gérer l'identification
    etat = {"frame_courant": None, "visages_detectes": 0, "identifie": False}
    
    # Canvas pour afficher la caméra
    canvas = Canvas(frame_principal, bg="black", width=400, height=300)
    canvas.pack(pady=10)
    
    # Label pour afficher le statut
    label_statut = Label(frame_principal, text="En attente...", font=("Arial", 12), bg="lightgreen", fg="blue")
    label_statut.pack(pady=5)
    
    # Label pour afficher le résultat
    label_resultat = Label(frame_principal, text="", font=("Arial", 14, "bold"), bg="lightgreen")
    label_resultat.pack(pady=10)
    
    def mettre_a_jour_camera():
        """Mettre à jour l'affichage de la caméra en temps réel"""
        ret, frame = cap.read()
        if not ret:
            return
        
        # Redimensionner pour plus rapide
        frame = cv2.resize(frame, (400, 300))
        
        # Convertir en niveaux de gris pour la détection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détecter les visages
        faces = detector.detectMultiScale(gray, 1.3, 5)
        etat["visages_detectes"] = len(faces)
        
        # Dessiner les rectangles pour les visages détectés
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Afficher le nombre de visages détectés
        texte_visages = f"Visages détectés: {len(faces)}"
        cv2.putText(frame, texte_visages, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Convertir pour Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        from PIL import Image, ImageTk
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        # Afficher sur le canvas
        canvas.create_image(0, 0, anchor=NW, image=img_tk)
        canvas.image = img_tk  # Garder une référence
        
        # Sauvegarder le frame actuel
        etat["frame_courant"] = gray
        
        # Mettre à jour le statut
        if len(faces) > 0:
            label_statut.config(text="✓ Visage détecté! Cliquez sur IDENTIFIER", fg="green")
        else:
            label_statut.config(text="✗ Pas de visage détecté", fg="red")
        
        # Appeler à nouveau dans 30ms
        frame_principal.after(30, mettre_a_jour_camera)
    
    def identifier():
        """Identifier la personne quand on clique sur le bouton"""
        if etat["frame_courant"] is None or etat["visages_detectes"] == 0:
            messagebox.showerror("Erreur", "Pas de visage détecté!")
            return
        
        # Détecter à nouveau le visage dans le frame actuel
        gray = etat["frame_courant"]
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            messagebox.showerror("Erreur", "Visage disparu!")
            return
        
        # Utiliser le premier visage détecté
        (x, y, w, h) = faces[0]
        visage = gray[y:y+h, x:x+w]
        
        # Essayer de reconnaître
        label, confiance = recognizer.predict(visage)
        
        # Afficher la confiance pour déboguer
        print(f"Confiance: {confiance:.2f}, Label: {label}, Nom: {label_map.get(label, 'Inconnu')}")
        
        # Si la confiance est faible (< 100), on reconnaît la personne
        # IMPORTANT: Plus petit = meilleur (< 100 = assez sûr)
        if confiance < 100:
            nom = label_map[label]
            solde = soldes.get(nom, 0)
            
            # Débiter 5€
            if solde >= 5:
                soldes[nom] = solde - 5
                with open("soldes.json", "w") as f:
                    json.dump(soldes, f)
                
                # Afficher le message de succès
                label_resultat.config(
                    text=f"✓ Bienvenue {nom}!\n{solde:.2f}€ → {soldes[nom]:.2f}€",
                    fg="green"
                )
                messagebox.showinfo("Succès", f"Bienvenue {nom}!\nSolde: {soldes[nom]:.2f}€")
            else:
                # Pas assez d'argent
                label_resultat.config(
                    text=f"✗ Solde insuffisant: {solde:.2f}€",
                    fg="red"
                )
                messagebox.showerror("Erreur", f"Solde insuffisant: {solde:.2f}€")
        else:
            # Visage non reconnu
            label_resultat.config(
                text=f"✗ Visage non reconnu (confiance: {confiance:.1f})",
                fg="red"
            )
            messagebox.showerror("Erreur", f"Visage non reconnu!\nConfiance: {confiance:.1f}")
    
    # Bouton pour identifier
    Button(frame_principal, text="IDENTIFIER", font=("Arial", 14), bg="green", fg="white", width=25, command=identifier).pack(pady=10)
    
    # Bouton pour revenir au menu
    Button(frame_principal, text="Retour", font=("Arial", 12), bg="gray", fg="white", width=25, command=lambda: (cap.release(), cv2.destroyAllWindows(), menu_principal())).pack(pady=5)
    
    # Démarrer la mise à jour de la caméra
    mettre_a_jour_camera()

# ====================================================================
# LANCER L'APPLICATION
# ====================================================================
# Ce code s'exécute quand le programme démarre

if __name__ == "__main__":
    # Créer la fenêtre principale
    fenetre = Tk()
    fenetre.title("Restaurant")
    fenetre.geometry("500x400")
    fenetre.configure(bg="lightblue")
    
    # Créer le frame principal (le cadre qui contient l'interface)
    frame_principal = Frame(fenetre, bg="lightblue")
    frame_principal.pack(fill=BOTH, expand=True)
    
    # Afficher le menu principal au démarrage
    menu_principal()
    
    # Lancer la boucle principale (écouter les événements de souris/clavier)
    fenetre.mainloop()
