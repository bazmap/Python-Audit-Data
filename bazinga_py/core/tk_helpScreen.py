# -*-coding:Utf-8 -*

# Interface de l'aide
# Le contenu ne doit pas changer

# Modules requis
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from bazinga_py.core.init_framework import functions
from bazinga_py.core.init_framework import app_var as app_var
from bazinga_py.core import tk_resources as ba_tk


# Ecran d'accueil
class helpScreen(ba_tk.Toplevel):
	def __init__(self, parent=None):
		ba_tk.Toplevel.__init__(self, parent)

		# Définition de variables de classe
		self.defVariable()
		# Définition des paramètres de la fenêtre du programme
		self.setWindowParam()
		# Définition des widgets
		self.setWidget()
		# Recalcul des dimensions
		self.update()
		self.geometry('1000' + 'x' + str(self.widget['frame'].winfo_height() + 20))
		# Positionnement au centre de l'écran
		self.centerScreen()



	# Définition de variables de classe
	def defVariable(self):
		# Quelques variables
		self.widget = dict()

		# Polices
		self.font_custom_title = tkFont.Font(
			family = tkFont.nametofont("TkDefaultFont").actual()['family'],
			size = tkFont.nametofont("TkDefaultFont").actual()['size'],
			weight = "bold",
			slant = "roman"
		)
		self.font_custom_parameter = tkFont.Font(
			family = tkFont.nametofont("TkDefaultFont").actual()['family'],
			size = tkFont.nametofont("TkDefaultFont").actual()['size'],
			weight = "bold",
			slant = "roman"
		)
		self.font_custom_value = tkFont.Font(
			family = functions.checkFontAvailability('Consolas', 'Menlo', 'DejaVu Sans Mono'),
			size = tkFont.nametofont("TkDefaultFont").actual()['size'],
			weight = "normal",
			slant = "roman"
		)



	# Définition des paramètres de la fenêtre du programme
	def setWindowParam(self):

		# Titre de la fenêtre
		self.title('Aide')

		# Icone de l'application		
		self.softwareIcon = tk.PhotoImage(file = app_var['software']['icon'])
		self.iconphoto(False, self.softwareIcon)

		# Au dessus
		self.putOnTop()

		# Taille maximale
		self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight() - (31 + 30))

		# Taille d'ouverture
		self.geometry('1400x1000')



	# Définition des widgets
	def setWidget(self):

		# Création d'un caneva
		self.widget['canvas'] = tk.Canvas(
			self,
			borderwidth = 0,
			highlightthickness = 0
		)
		self.widget['canvas'].pack(
			side=tk.LEFT,
			fill = "both", 
			expand = True,
			pady = 10
		)



		# Création d'une barre de défilement
		self.widget['scrollbar'] = tk.Scrollbar(
			self
		)
		self.widget['scrollbar'].pack(
			side=tk.RIGHT,
			fill = 'y'
		)



		# Création d'un cadre
		self.widget['frame'] = ttk.Frame(
			self.widget['canvas']
		)
		self.widget['frame'].pack(
			fill = "both", 
			expand = True
		)

		self.widget['frame'].columnconfigure(
			0,
			weight = 1
		)
		self.widget['frame'].columnconfigure(
			1,
			weight = 1
		)

		self.widget['frame'].columnconfigure(
			0,
			weight = 1
		)
		self.widget['frame'].columnconfigure(
			1,
			weight = 1
		)



		# Configuration du défilement
		# Récupération de la zone défilable
		self.widget['frame'].bind(
			"<Configure>",
			lambda e: self.widget['canvas'].configure(
				scrollregion=self.widget['canvas'].bbox("all")
			)
		)
		# Création d'une fenêtre de cadre dans le caneva
		self.widget['canvas'].create_window(
			(0, 0), 
			window = self.widget['frame'], 
			anchor="nw"
		)
		# Définition de la scrollbar comme bare de défilement du caneva
		self.widget['canvas'].configure(
			yscrollcommand = self.widget['scrollbar'].set
		)
		self.widget['scrollbar'].configure(
			command = self.widget['canvas'].yview
		)
		# Défilement via la souris
		functions.set_mousewheel(self.widget['canvas'])



		# Listing des paramètres utilisables
		for iteration, my_param in enumerate(app_var['param']['software']):

			if app_var['param']['software'][my_param]['input_scope'] != []:

				# Ajout d'un titre
				self.widget[my_param + '_titre'] = ttk.Label(
					self.widget['frame'],
					text = my_param,
					width = 30,
					anchor = "e",
					font = self.font_custom_title
				)
				self.widget[my_param + '_titre'].grid(
					row = iteration, 
					column = 0, 
					sticky = "ne"
				)

				# Ajout de la définition
				self.widget[my_param + '_def'] = ba_tk.Text(
					self.widget['frame'],
					width = 110,
					cursor = 'arrow',
					relief = 'flat',
					wrap = 'word',
					borderwidth = 0
				)
				self.widget[my_param + '_def'].grid(
					row = iteration, 
					column = 1, 
					sticky = "nw",
					padx = 10,
					pady = (0, 5)
				)

				# Définition :
				if 'default_user' in app_var['param']['software'][my_param]:
					default_value = str(app_var['param']['software'][my_param]['value_user'] or 'None')
				else:
					default_value = str(app_var['param']['software'][my_param]['value'] or 'None')

				self.widget[my_param + '_def'].insert('end', app_var['param']['software'][my_param]['help'])

				self.widget[my_param + '_def'].insert('end', '\n' + 'Valeur attendue : ', "parametre")
				self.widget[my_param + '_def'].insert('end', app_var['param']['software'][my_param]['type'] + ' - ' + app_var['param']['software'][my_param]['expected'], 'valeur')

				self.widget[my_param + '_def'].insert('end', '\n' + 'Valeur par défaut : ', "parametre")
				self.widget[my_param + '_def'].insertResize('end', default_value, 'valeur')


				self.widget[my_param + '_def'].tag_config(
					"parametre",
					font = self.font_custom_parameter
				)
				self.widget[my_param + '_def'].tag_config(
					"valeur",
					font = self.font_custom_value
				)

	# Fonction de fermeture de l'écran
	def closeScreen(self, event):
		self.destroy()