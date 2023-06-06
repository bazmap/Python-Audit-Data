# -*-coding:Utf-8 -*

# Interface de l'écran d'accueil
# Le contenu ne doit pas changer

# Modules requis
import tkinter as tk
import tkinter.font as tkFont

from bazinga_py.core.init_framework import app_var
from bazinga_py.core import tk_resources as ba_tk



# Ecran d'accueil
class splashScreen(ba_tk.Toplevel):
	def __init__(self, parent):
		ba_tk.Toplevel.__init__(self, parent)

		# Définition de variables de classe
		self.defVariable()
		# Définition des paramètres de la fenêtre du programme
		self.setWindowParam()
		# Définition des widgets
		self.setWidget()
		# Positionnement au centre de l'écran
		self.centerScreen()



	# Définition de variables de classe
	def defVariable(self):
		# Quelques variables
		# Polices
		self.font_custom_title = tkFont.Font(
			family = tkFont.nametofont("TkDefaultFont").actual()['family'],
			size = 26,
			weight = "bold",
			slant = "roman"
		)
		self.font_custom_version = tkFont.Font(
			family = tkFont.nametofont("TkDefaultFont").actual()['family'],
			size = 16,
			weight = "normal",
			slant = "roman"
		)
		self.font_custom_message = tkFont.Font(
			family = tkFont.nametofont("TkDefaultFont").actual()['family'],
			size = tkFont.nametofont("TkDefaultFont").actual()['size'] + 2,
			weight = "normal",
			slant = "italic"
		)

		# Couleurs
		self.color_background = "#0099FF"
		self.color_foreground = "#fff"

		# Image du splash screen
		self.splashImage = tk.PhotoImage(file = app_var['software']['splash_screen'])
		self.windowWidth = self.splashImage.width()
		self.windowHeight = self.splashImage.height()



	# Définition des paramètres de la fenêtre du programme
	def setWindowParam(self):
		# Taille de la fenêtre
		#self.geometry(str(self.windowWidth) + 'x' + str(self.windowHeight))

		# Suppression des contours
		self.overrideredirect(True)

		# Au dessus
		self.putOnTop(True)



	# Définition des widgets
	def setWidget(self):

		# Canvas
		self.canvas = tk.Canvas(
			self,
			width = self.windowWidth,
			height = self.windowHeight,
			borderwidth = 0,
			highlightthickness = 0,
			background = self.color_background
		)
		self.canvas.pack(
			fill = "both", 
			expand = True
		)

		# Ajout d'une image
		self.canvasImage = self.canvas.create_image(
			0,
			0,
			image = self.splashImage,
			anchor = "nw"
		)


		# Ajout du titre
		self.canvasTitle = self.canvas.create_text(
			self.windowWidth - 10,
			100,
			anchor = "ne",
			text = app_var['software']['name'],
			fill = self.color_foreground,
			font = self.font_custom_title,
			justify = 'right',
			tags = 'title'
		)

		# Ajout de la version
		self.canvasVersion = self.canvas.create_text(
			self.windowWidth - 10,
			self.canvas.bbox(self.canvasTitle)[3] - 5,
			anchor = "ne",
			text = 'v' + app_var['software']['version'],
			fill = self.color_foreground,
			font = self.font_custom_version,
			justify = 'right',
			tags = 'title'
		)

		# Ajout d'un texte
		self.canvasMessage = self.canvas.create_text( 
			self.windowWidth / 2,
			self.windowHeight - 10,
			anchor = "s",
			text = "Chargement...",
			fill = self.color_foreground,
			font = self.font_custom_message,
			justify = 'center',
			tags = 'message'
		)