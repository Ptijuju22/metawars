# -*- coding: utf-8 -*-

"""
	Contient une classe permettant de créer une fenêtre et de gérer les images.
"""


import constantes
import utile
import niveau
from widgets import Texte, Bouton, Image

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import sys
import pygame


class Affichage(object):
	""" Permet de créer une fenêtre, charger des images et gérer des Widgets. """

	def __init__(self):
		""" Initialise un nouvel affichage. """

		# on cree une fenetre
		self.fenetre = pygame.display.set_mode(constantes.General.TAILLE_ECRAN)
		self.images = {}
		self.widgets = []

		# on defini un titre a notre fenetre (ici: MetaWars)
		pygame.display.set_caption(constantes.General.NOM)
		icone = pygame.image.load(constantes.General.IMAGE_ICONE)
		pygame.display.set_icon(icone)

	def charger_images(self):
		""" Charge les images du disque dur en mémoire vive. Il est préférable 
			de n'appeler cette méthode qu'une seule fois pour éviter de ralentir le jeu. """

		utile.debogguer("Chargement des images...")

		# Pour chaque image dans constantes.IMAGES
		for chemin_image in constantes.Ressources.IMAGES:
			chemin_image = os.path.join(constantes.Chemin.IMAGES, *chemin_image)

			try:
				self.images[chemin_image] = pygame.image.load(chemin_image)
				utile.debogguer("L'image '" + chemin_image + "' a été chargé !")
			except pygame.error:
				utile.debogguer("L'image '" + chemin_image + "' n'existe pas !", 1)
		
		utile.debogguer("Fin du chargement des images !")

	def obtenir_image(self, chemin_image):
		""" Renvoie une surface pygame à un emplacement défini. Si l'image n'a pas été 
			chargée, crée une nouvelle surface noire. 

			<chemin_image> (str): L'emplacement de l'image. """

		if chemin_image in self.images:
			# si l'image existe, on la renvoie
			return self.images[chemin_image].convert_alpha()
		else:
			# sinon, on renvoie une surface noire de 50x50 pixels
			return pygame.Surface((50, 50))

	def supprimer_widgets(self):
		""" Supprime tous les widgets de cet affichage en vidant la liste des widgets. """

		self.widgets.clear() # vide la liste des widgets de cet affichage

	def creer_widgets_partie(self):
		""" Crée les textes à afficher pendant la partie renseignant sur le temps écoulé,
			les pièces amassées, la vie restante, les dégats et vitesse bonus. """

		texte_temps = Texte(self, "Temps: 0s", (10, 10))
		texte_pieces = Texte(self, "Pièces: 0", (10, 40))
		texte_vie = Texte(self, "Vie: 0", (10, 70))

		texte_arme = Texte(self, "Bonus dégats: 0", (constantes.General.TAILLE_ECRAN[0] - 10, 10), ancrage=(1, -1))
		texte_vitesse = Texte(self, "Bonus vitesse: x1", (constantes.General.TAILLE_ECRAN[0] - 10, 40), ancrage=(1, -1))
		
		self.widgets.append(texte_temps)
		self.widgets.append(texte_pieces)
		self.widgets.append(texte_vie)

		self.widgets.append(texte_arme)
		self.widgets.append(texte_vitesse)

	def creer_widgets_menu(self, jeu):
		""" Crée un bouton 'Jouer', un bouton 'Quitter', une image de titre et des textes informatifs. """

		def jouer():
			jeu.initialiser_partie()
			jeu.lancer_boucle()

		def multijoueur():
			jeu.initialiser_menu_multijoueur()
			jeu.lancer_boucle()

		def quitter():
			jeu.arreter()

		milieu_ecran_x = constantes.General.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.General.TAILLE_ECRAN[1] // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		bouton_jouer = Bouton(self, jouer, "Jouer en solo", position=(milieu_ecran_x, milieu_ecran_y), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_multi = Bouton(self, multijoueur, "Multijoueur", position=(milieu_ecran_x, milieu_ecran_y+80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_quitter = Bouton(self, quitter, "Quitter", position=(milieu_ecran_x, milieu_ecran_y+160), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		logo = Image(self, constantes.General.IMAGE_TITRE, position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_version = Texte(self, "v" + __version__, position=(10, constantes.General.TAILLE_ECRAN[1] - 10), \
			ancrage=(-1, 1), taille_police=16)
		texte_dev = Texte(self, __author__, \
			position=(constantes.General.TAILLE_ECRAN[0] - 10, constantes.General.TAILLE_ECRAN[1] - 10), \
			ancrage=(1, 1), taille_police=16)

		self.widgets.append(bouton_jouer)
		self.widgets.append(bouton_multi)
		self.widgets.append(bouton_quitter)
		self.widgets.append(logo)
		self.widgets.append(texte_version)
		self.widgets.append(texte_dev)

	def creer_widgets_multijoueur(self, jeu):
		def heberger():
			jeu.heberger_partie()

		def rejoindre():
			jeu.rejoindre_partie()

		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		milieu_ecran_x = constantes.General.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.General.TAILLE_ECRAN[1] // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		bouton_heberger = Bouton(self, heberger, "Héberger", position=(milieu_ecran_x, milieu_ecran_y), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_rejoindre = Bouton(self, rejoindre, "Rejoindre", position=(milieu_ecran_x, milieu_ecran_y+80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_retour = Bouton(self, retour, "Retour", position=(milieu_ecran_x, milieu_ecran_y+160), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		logo = Image(self, constantes.General.IMAGE_TITRE, position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))

		self.widgets.append(bouton_heberger)
		self.widgets.append(bouton_rejoindre)
		self.widgets.append(bouton_retour)
		self.widgets.append(logo)

	def creer_widgets_pause(self, jeu):
		def continuer():
			jeu.geler_partie(False)

		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		milieu_ecran_x = constantes.General.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.General.TAILLE_ECRAN[1] // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		bouton_continuer = Bouton(self, continuer, "Continuer", position=(milieu_ecran_x, milieu_ecran_y), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		bouton_menu = Bouton(self, retour, "Retour au menu principal", position=(milieu_ecran_x, milieu_ecran_y+80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		logo_pause = Image(self, constantes.General.IMAGE_TITRE, position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		texte_pause = Texte(self, "Pause", position=(milieu_ecran_x, milieu_ecran_y - 40), \
			ancrage=(0, 0), taille_police=18)

		self.widgets.append(bouton_continuer)
		self.widgets.append(bouton_menu)
		self.widgets.append(logo_pause)
		self.widgets.append(texte_pause)

	def creer_widgets_fin(self, jeu):
		def retour():
			jeu.arreter_boucle()
			jeu.initialiser_menu_principal()

		milieu_ecran_x = constantes.General.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.General.TAILLE_ECRAN[1] // 2
		milieu_du_milieu_ecran_y = milieu_ecran_y // 2

		texte_fin = Texte(self, "Pièces: {} | Temps: {}s".format(jeu.niveau.pieces, round(jeu.niveau.temps_total)), \
			position=(milieu_ecran_x, milieu_ecran_y), ancrage=(0, 0), taille_police=18)
		bouton_menu = Bouton(self, retour, "Retour au menu principal", position=(milieu_ecran_x, milieu_ecran_y + 80), \
			taille=(300, 50), ancrage=(0, 0), taille_police=20)
		logo_fin = Image(self, constantes.General.IMAGE_TITRE, position=(milieu_ecran_x, milieu_du_milieu_ecran_y), \
			taille=(400, 80), ancrage=(0, 0))
		titre_fin = Texte(self, "Game Over", position=(milieu_ecran_x, milieu_ecran_y - 40), \
			ancrage=(0, 0), taille_police=18)

		self.widgets.append(texte_fin)
		self.widgets.append(bouton_menu)
		self.widgets.append(logo_fin)
		self.widgets.append(titre_fin)

	def supprimer_widgets_pause(self):
		for _ in range(4):
			self.widgets.pop()

	def actualiser(self, niveau, jeu):
		""" Efface la fenêtre, redessine le terrain, les entités, puis les widgets en les actualisant. 

			<niveau> (niveau.Niveau): Le niveau à afficher
			<en_partie> (bool): Si True, actualise les textes affichant les stats du joueur """

		# On rend tous les pixels de la fenetre blanc
		self.fenetre.fill((255, 255, 255))
		# on affiche le fond du niveau
		self.afficher_carte(niveau)
		# on affiche les entités
		for entite in niveau.entites:
			self.afficher_entite(entite)
		# si on est en partie, on acalise le score
		if jeu.en_partie:
			# on actualise le score en fonction de celui du niveau
			self.actualiser_scores(niveau)
		# on redessine les widgets
		self.afficher_widgets()
		# On actualise l'écran
		pygame.display.update()

	def actualiser_evenements(self, jeu):
		""" Lit les évenements du clavier et de la souris et exécute les fonctions associées
			à certaines touches (ex: Appui sur la touche Z -> le joueur monte).

			<niveau> (niveau.Niveau): Le niveau à actualiser en fonction des actions utilisateur.
			<en_partie> (bool): si True, fait bouger et tirer le joueur, sinon le joueur ne réagit pas. """

		# on parcourt l'ensemble des evenements utilisateurs (clic, appui sur une touche, etc)
		for evenement in pygame.event.get():
			# si l'utilisateur a cliqué sur la croix rouge de la fenêtre
			# on arrete le jeu
			if evenement.type == pygame.QUIT:
				jeu.arreter()
			# sinon si on est en partie (et pas dans le menu principal)
			elif jeu.en_partie:
				jeu.niveau.actualiser_evenement(evenement)
			# on actualise les évenements pour chaque widget
			for widget in self.widgets:
				widget.actualiser_evenement(evenement)

	def afficher_entite(self, entite):
		""" Affiche une entité en fonction de ses attributs de position, taille et rotation.

			<entite> (entites.Entite): L'entité à afficher. """

		joueur = entite.niveau.obtenir_joueur_local()
		# on recuper le milieu de l'ecran
		milieu_ecran_x = constantes.General.TAILLE_ECRAN[0] // 2
		milieu_ecran_y = constantes.General.TAILLE_ECRAN[1] // 2

		# on recupere le milieu de l'entite
		milieu_entite_x = entite.taille[0] * constantes.General.ZOOM / 2
		milieu_entite_y = entite.taille[1] * constantes.General.ZOOM / 2

		# on calcul la position de l'entité par rapport au joueur
		# car celui-ci doit être centré en plein milieu de l'écran
		entite_x = (entite.position[0] - joueur.position[0]) * constantes.General.ZOOM + milieu_ecran_x
		entite_y = (entite.position[1] - joueur.position[1]) * constantes.General.ZOOM + milieu_ecran_y

		# on applique une rotation sur l'image en fonction de l'angle de l'entite
		# mais il faut d'abord convertir l'angle de l'entite en degrés (pygame travaille avec des degrés)
		angle_degres = utile.radian_en_degres(entite.angle)
		image_tournee = pygame.transform.rotate(entite.image, angle_degres)

		# la taille de l'image a peut-être changé en la tournant
		# il faut donc calculer la différence de taille entre les 2 images
		d_taille_x = image_tournee.get_size()[0] - entite.image.get_size()[0]
		d_taille_y = image_tournee.get_size()[1] - entite.image.get_size()[1]

		# on peut maintenant déterminer la position de l'image
		x = int(entite_x - milieu_entite_x - d_taille_x / 2)
		y = int(entite_y - milieu_entite_y - d_taille_y / 2)

		# on colle l'image de l'entité
		self.fenetre.blit(image_tournee, (x, y))

	def afficher_carte(self, niveau):
		""" Dessine le fond du niveau en fonction de la position du joueur pour donner
			l'impression que celui-ci bouge alors qu'il reste constament centré en plein
			milieu de l'écran. 

			<niveau> (niveau.Niveau): Le niveau à afficher. """

		largeur, hauteur = niveau.image.get_size()
		joueur_x, joueur_y = niveau.obtenir_joueur_local().position

		distance_joueur_x = (joueur_x * constantes.General.ZOOM) % largeur
		distance_joueur_y = (joueur_y * constantes.General.ZOOM) % hauteur

		# on calcule le nombre de texture qu'il va falloir afficher à l'écran
		# en largeur (x) et en hauteur (y)
		# math.ceil renvoie la valeur arrondi supérieure ou égale
		# car il vaut mieux afficher des textures en trop que pas assez
		# sinon il va rester du vide
		nb_texture_x = math.ceil(constantes.General.TAILLE_ECRAN[0] / largeur)
		nb_texture_y = math.ceil(constantes.General.TAILLE_ECRAN[1] / hauteur)

		if distance_joueur_x != 0:
			nb_texture_x += 1
		if distance_joueur_y != 0:
			nb_texture_y += 1

		for x in range(nb_texture_x):
			for y in range(nb_texture_y):
				self.fenetre.blit(niveau.image, (x * largeur - distance_joueur_x, y * hauteur - distance_joueur_y))

	def afficher_widgets(self):
		""" Redessine tous les widgets de cet affichage. """

		for widget in self.widgets:
			widget.actualiser()

	def actualiser_scores(self, niveau):
		""" Change le texte des Widgets affichant les stats du joueur. 

			<niveau> (niveau.Niveau): Le niveau dont il faut afficher les stats. """

		texte_temps = self.widgets[0]
		texte_pieces = self.widgets[1]
		texte_vie = self.widgets[2]
		texte_arme = self.widgets[3]
		texte_vitesse = self.widgets[4]

		joueur = niveau.obtenir_joueur_local()

		texte_temps.texte = "Temps: {temps}s".format(temps=int(niveau.temps_total))
		texte_pieces.texte = "Pièces: {pieces}".format(pieces=niveau.pieces)
		texte_vie.texte = "Vie: {vie}".format(vie=int(joueur.vie))
		
		texte_arme.texte = "Bonus dégats: {degats}".format(degats=joueur.degats_bonus)
		texte_vitesse.texte = "Bonus vitesse: x{vitesse}".format(vitesse=round(joueur.vitesse, 2))