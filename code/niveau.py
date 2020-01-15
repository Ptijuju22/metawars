# -*- coding: utf-8 -*-

import constantes
from entites import Joueur, Ennemi, Bonus

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import os
import pygame
import random


class Niveau(object):
	""" Gère l'ensemble des entités du jeu ainsi que certaines données de partie. """

	def __init__(self, affichage):
		self.image = None
		self.affichage = affichage
		self.entites = []
		self.pieces = 0
		self.temps_total = 0
		self.en_pause = False

	def cree_joueur(self):
		joueur = Joueur(self)
		joueur.charge_image()
		self.entites.append(joueur)

	def obtenir_joueur_local(self):
		if self.entites:
			if type(self.entites[0]) == Joueur:
				return self.entites[0]
		return Joueur(self)

	def charge_image(self):
		""" Charge l'image de fond et celle du joueur. """

		# on charge le fond du niveau
		self.image = self.affichage.obtenir_image(constantes.General.IMAGE_FOND)

	def actualise(self, temps):
		""" Actualise les entités et tente de faire apparaitre des bonus et des ennemis.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		if not self.en_pause:
			self.temps_total += temps
			
			for entite in self.entites:
				entite.actualise(temps)

			self.fait_apparaitre(temps)

	def fait_apparaitre(self, temps):
		""" Fait parfois apparaitre un bonus et/ou un ennemi.

			<temps> (float): Le temps écoulé depuis la dernière actualisation. """

		# on pioche un nombre aléatoire
		nb = random.random()

		# si le nombre pioché est inférieur au temps écoulé divisé 
		# par la fréquence moyenne d'apparition...
		if nb <= temps / constantes.Ennemi.FREQUENCE_APPARITION:
			# on crée un ennemi
			self.cree_ennemi()

		# pareil pour les bonus
		nb = random.random()

		if nb <= temps / constantes.Bonus.FREQUENCE_APPARITION:
			self.cree_bonus()

	def enleve_entite(self, entite):
		""" Enlève une entité donnée de la liste des entités. 

			<entite> (entites.Entite): L'entité à enlever. """

		# si l'entité fait bien parti de la liste des entités de ce niveau
		if entite in self.entites:
			# on la retire de la liste (elle ne fait donc plus parti du niveau)
			self.entites.remove(entite)

	def cree_bonus(self):
		""" Crée un nouveau bonus à une position aléatoire proche du joueur. """

		# on crée un bonus
		bonus = Bonus(self)
		joueur = self.obtenir_joueur_local()

		# on choisi aléatoirement la distance entre le joueur et le bonus
		dx = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Bonus.DIS_MAX

		# on redéfinit la position du Bonus autour le joueur
		bonus.position[0] = joueur.position[0] + dx
		bonus.position[1] = joueur.position[1] + dy

		# on lui fait charger son image
		bonus.charge_image()

		# on ajoute le bonus a la liste des entités
		self.entites.append(bonus)

	def cree_ennemi(self):
		""" Crée un nouvel ennemi à une position aléatoire proche du joueur. """

		# on crée un ennemi
		ennemi = Ennemi(self)
		joueur = self.obtenir_joueur_local()
		
		# on choisi aléatoirement la distance entre l'ennemi et le joueur
		dx = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		dy = (random.random() - 0.5) * 2 * constantes.Ennemi.DIS_MAX
		# on redéfinit la position de l'ennemi autour du joueur
		ennemi.position[0] = joueur.position[0] + dx
		ennemi.position[1] = joueur.position[1] + dy

		# on lui fait charger ses images
		ennemi.charge_image()
		# on ajoute l'ennemi a la liste des entités
		self.entites.append(ennemi)

	def termine(self):
		""" Met en pause le niveau. """

		self.en_pause = True
		print("La partie s'est terminée avec {pieces} pièces après {temps} seconde(s) de jeu" \
			.format(pieces=self.pieces, temps=self.temps_total))