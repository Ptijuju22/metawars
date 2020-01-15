# -*- coding: utf-8 -*-

import constantes

__author__ = "Gabriel Neny; Colin Noiret; Julien Dubois"
__version__ = "0.1.0"

import math
import os
import sys
import datetime


def arreter():
	""" Arrête le jeu en tuant le programme. """
	deboggue("Arrêt de " + constantes.General.NOM + "...")
	sys.exit()


def lire_fichier(chemin_fichier):
	""" Permet de lire un fichier à un emplacement donné. 

		<chemin_fichier> (str): Le chemin du fichier. """

	# On teste si le fichier existe bel et bien
	if os.path.exists(chemin_fichier):
		# si oui, on l'ouvre en mode lecture ("r")
		# et on le stocke dans la variable 'fichier'
		with open(chemin_fichier, "r") as fichier:
			# on retourne son contenu avec la methode read()
			return fichier.read()
	else:
		deboggue("Le fichier '" + chemin_fichier + "' est introuvable !", 1)
		return False


def ecrire_fichier(chemin_fichier, contenu):
	""" Permet d'écrire du texte dans un fichier à un emplacement spécifique.
		Le fichier sera créé si il n'existe pas, sinon il sera effacé puis recréé.

		<chemin_fichier> (str): Le chemin du fichier.
		<contenu> (str): Le texte à écrire dans le fichier. """

	# On ouvre le fichier en mode écriture ("w")
	# et on le stocke dans la variable 'fichier'
	with open(chemin_fichier, "w") as fichier:
		fichier.write(contenu)


def radian_en_degres(angle):
	""" Convertit un angle en radian, en degré.

		<angle> (float): L'angle en radian à convertir. """
	return angle * 180 / math.pi


def degres_en_radian(angle):
	""" Convertit un angle en degré, en radian.

		<angle> (float): L'angle en degré à convertir. """
	return angle * math.pi / 180


def deboggue(message, niveau_erreur=0):
	if constantes.General.DEBUG:
		s = "[{h}:{m}:{s}] [{e}] {t}"
		d = datetime.datetime.now()
		print(s.format(h=d.hour, m=d.minute, s=d.second, e=constantes.General.ERREURS[niveau_erreur], t=message))