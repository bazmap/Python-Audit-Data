# -*-coding:Utf-8 -*

# Interface graphique du programme
# Le contenu ne doit pas changer

# Modules requis
import os
import copy
import tkinter as tk
from tkinter import filedialog as fd

from bazinga_py.core.init_framework import functions
from bazinga_py.core.init_framework import app_var
from bazinga_py.core.init_framework import logger
from bazinga_py.core import config_file_parser
from bazinga_py.core import tk_resources as ba_tk
from bazinga_py.core import tk_rootMenuBar
from bazinga_py.core import tk_splashScreen
from bazinga_py.core import tk_infoScreen
from bazinga_py.core import tk_helpScreen



# Création d'une classe de définition de l'interface graphique
class rootWindows(ba_tk.Tk):
	def __init__(self, openSplashScreen = True):
		ba_tk.Tk.__init__(self)

		logger.info('Initialisation de l''interface')

		# Démarrage de l'écran d'accueil
		if openSplashScreen == True:
			logger.info("Démarrage écran d'accueil")
			self.openSplashScreen()

		# Définition des paramètres de la fenêtre du programme
		logger.info("Chargement des paramètres de la fenêtre du programme")
		self.setWindowParam()

		# Mise en place de la barre de menu
		self.setMenuBar()

		# Définition des variables des widget
		self.setWidgetVar()



	# Définition des paramètres de la fenêtre du programme
	def setWindowParam(self):
		# Titre de l'application
		self.title(app_var['software']['name'] + ' - ' + app_var['software']['version'])

		# Icone de l'application
		#self.iconbitmap(app_var['software']['logo'])
		#self.iconphoto(False, tk.PhotoImage(file='my_icon.ico'))
		
		self.softwareIcon = tk.PhotoImage(file = app_var['software']['icon'])
		self.iconphoto(False, self.softwareIcon)

		# Définition du thème
		self.tk.call("source", os.path.join(app_var['framework']['dir'], 'theme', "azure.tcl"))
		self.tk.call("set_theme", "light")

		# Taille minimale
		self.minsize(400, 400)
		# Taille de l'application
		self.geometry(str(app_var['software']['size']['x']) + 'x' + str(app_var['software']['size']['y']))



	def run_mainloop(self):

		# Positionnement au centre de l'écran
		self.centerScreen()

		# Suppression de l'écran d'accueil
		self.after(2000, logger.info("Fermeture écran d'accueil"))
		self.after(000, self.splashScreen.destroy)
		self.after(000, self.focus_force)

		self.mainloop()



	# Affichage de l'écran d'accueil
	def openSplashScreen(self):
		self.splashScreen = tk_splashScreen.splashScreen(self)



	# Affichage de l'écran d'aide
	def openHelpScreen(self):
		self.helpScreen = tk_helpScreen.helpScreen(self)



	# Affichage du panneau d'information
	def openInfoScreen(self):
		self.infoScreen = tk_infoScreen.infoScreen(self, True)



	# Fonction d'association des variables de configuration aux variables tkinter
	def setWidgetVar(self):

		app_var['param']['init_tk'] = dict()


		for key in (app_var['param']['init']):

			app_var['param']['init_tk'][key] = copy.deepcopy(app_var['param']['init'][key])
			app_var['param']['init_tk'][key].pop('value')

			if 'type' not in app_var['param']['init'][key]:
				app_var['param']['init'][key]['type'] = 'string';


			if app_var['param']['init'][key]['type'] == 'boolean':
				app_var['param']['init_tk'][key]['value'] = tk.BooleanVar()
				app_var['param']['init_tk'][key]['value'].set(bool(app_var['param']['init'][key]['value']))

			elif app_var['param']['init'][key]['type'] == 'integer':
				app_var['param']['init_tk'][key]['value'] = tk.IntVar()
				app_var['param']['init_tk'][key]['value'].set(int(app_var['param']['init'][key]['value'] or 0))

			elif app_var['param']['init'][key]['type'] == 'float':
				app_var['param']['init_tk'][key]['value'] = tk.DoubleVar()
				app_var['param']['init_tk'][key]['value'].set(float(app_var['param']['init'][key]['value'] or 0))

			else:
				app_var['param']['init_tk'][key]['value'] = tk.StringVar()
				app_var['param']['init_tk'][key]['value'].set(str(app_var['param']['init'][key]['value'] or ''))




	# Fonction d'association des variables de configuration aux variables tkinter
	def setMenuBar(self):

		# Ajout de la barre des menus
		self.rootMenuBar = tk_rootMenuBar.rootMenuBar(self)
		self.config(menu = self.rootMenuBar)

		self.bind(
			'<<menu_fichier-open_config_file>>', 
			self.open_config_file
		)
		self.bind(
			'<Control-o>',
			self.open_config_file
		)

		self.bind(
			'<<menu_fichier-save_config_file>>', 
			self.save_config_file
		)
		self.bind(
			'<Control-s>',
			self.save_config_file
		)




	def open_config_file(self, event = None):
		# Choix du fichier
		file = fd.askopenfilename(
			title = "Choisir un fichier de configuration",
			filetypes = [("Fichier de configuration", ".conf"), ("All files", ".*")],
			initialdir = app_var['software']['config_dir']
		)


		if file != '':
			# Récupération du fichier de configuration
			var_configParse = config_file_parser.configLoader(file)


			# Association à une variable
			for key in (var_configParse):

				if key not in app_var['param']['init_tk']:

					if key in app_var['param']['init']:
						if app_var['param']['init'][key]['type'] == 'boolean':
							app_var['param']['init_tk'][key]['value'] = tk.BooleanVar()
						elif app_var['param']['init'][key]['type'] == 'integer':
							app_var['param']['init_tk'][key]['value'] = tk.IntVar()
						elif app_var['param']['init'][key]['type'] == 'float':
							app_var['param']['init_tk'][key]['value'] = tk.DoubleVar()
						else:
							app_var['param']['init_tk'][key]['value'] = tk.StringVar()
					else:
						app_var['param']['init_tk'][key]['value'] = tk.StringVar()

				app_var['param']['init_tk'][key]['value'].set(var_configParse[key]['value'])



	def save_config_file(self, event = None):

		# Association à une variable
		for key in (app_var['param']['init_tk']):

			app_var['param']['init'][key]['value'] = (app_var['param']['init_tk'][key]['value'].get())

		config_file = functions.retrieveConfigFile(app_var['param']['init'], False)

		# Choix du fichier
		file = fd.asksaveasfilename  (
			title = "Sauvegarder la configuration",
			filetypes = [("Fichier de configuration", ".conf"), ("All files", ".*")],
			defaultextension = ".conf",
			initialfile = 'config',
			initialdir = app_var['software']['config_dir']
		)

		if file != '':
			with open(file, 'w', encoding='utf-8') as file_content:
				file_content.write(config_file)
