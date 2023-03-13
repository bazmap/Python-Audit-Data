# -*-coding:Utf-8 -*

# Barre de menu du programme
# Le contenu ne doit pas changer

# Modules requis
import tkinter as tk

from bazinga_py.core import tk_infoScreen
from bazinga_py.core import tk_helpScreen



# Création d'une classe de définition du menu
class rootMenuBar(tk.Menu):
	def __init__(self, parent):
		tk.Menu.__init__(self, parent)


		# Menu "Fichier"
		self.menu_fichier = tk.Menu(
			self,
			tearoff = 0
		)

		# Eléments
		self.menu_fichier.add_command(
			label = "Ouvrir un fichier de configuration",
			command = lambda: parent.event_generate('<<menu_fichier-open_config_file>>')
		)
		self.menu_fichier.add_command(
			label = "Sauvegarder la configuration",
			command = lambda: parent.event_generate('<<menu_fichier-save_config_file>>')
		)
		self.menu_fichier.add_separator()
		self.menu_fichier.add_command(
			label = "Quitter", 
			command = parent.quit
		)

		# Ajout du menu à la barre
		self.add_cascade(
			label = "Fichier", 
			menu = self.menu_fichier
		)



		# Menu "Aide"
		self.menu_aide = tk.Menu(
			self,
			tearoff = 0
		)

		# Eléments
		self.menu_aide.add_command(
			label = "Aide",
			command = self.openHelpScreen
		)
		self.menu_aide.add_separator()
		self.menu_aide.add_command(
			label = "A propos",
			command = self.openInfoScreen
		)

		# Ajout du menu à la barre
		self.add_cascade(
			label = "Aide", 
			menu = self.menu_aide
		)



	# Affichage de l'écran d'aide
	def openHelpScreen(self):
		self.helpScreen = tk_helpScreen.helpScreen(self)
		return self.helpScreen



	# Affichage du panneau d'information
	def openInfoScreen(self):
		self.infoScreen = tk_infoScreen.infoScreen(self, True)
		return self.infoScreen