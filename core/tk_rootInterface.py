# -*-coding:Utf-8 -*

# Interface graphique de la fenêtre principale



# Modules requis
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from bazinga_py.init import ba_app_var



# Définition d'une classe d'interface
class rootInterface(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		ttk.Frame.__init__(self, parent, *args, **kwargs)

		# Create widgets :)
		self.definition_widgets(parent)



	def definition_widgets(self, parent):

		s = ttk.Style()
		s.configure('new.TFrame', background='#7AC5CD')
		#, style='new.TFrame'

		# Cadre de base
		self.frame_base = ttk.Frame(self)
		self.frame_base.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = 0
		)


		# Onglets
		self.notebook = ttk.Notebook(self.frame_base)
		self.notebook.pack(
			fill = "both", 
			expand = True,
			padx = 5,
			pady = 5
		)






		# Onglet 1
		self.tab1 = ttk.Frame(self.notebook)
		self.tab1.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = (20, 0)
		)

		self.notebook.add(
			self.tab1, 
			text="Audit de fichier"
		)


		# Cadre 1
		self.tab1_frame1 = ttk.Frame(self.tab1)
		self.tab1_frame1.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = 0
		)
		self.tab1_frame1.columnconfigure(0, weight = 1)
		self.tab1_frame1.columnconfigure(1, weight = 5)
		self.tab1_frame1.columnconfigure(2, weight = 1)


		# emplacementDataAnalyse
		self.emplacementDataAnalyse_label = ttk.Label(
			self.tab1_frame1, 
			text = ba_app_var['param']['init']['emplacementDataAnalyse']['label']
		)
		self.emplacementDataAnalyse_label.grid(
			row = 1, 
			column = 0, 
			sticky = "e"
		)

		self.emplacementDataAnalyse_Entry = ttk.Entry(
			self.tab1_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['emplacementDataAnalyse']['value']
		)
		self.emplacementDataAnalyse_Entry.grid(
			row = 1, 
			column = 1, 
			sticky = "we"
		)
		self.emplacementDataAnalyse_Entry.xview_moveto(1)

		self.emplacementDataAnalyse_Button = ttk.Button(
			self.tab1_frame1, 
			text = 'Parcourir...',
			command = lambda : (
				self.select_dir(
					parent,
					ba_app_var['param']['init']['emplacementDataAnalyse']['value'],
					'emplacementDataAnalyse'
				)
			)
		)
		self.emplacementDataAnalyse_Button.grid(
			row = 1,
			column = 2,
			sticky = "w"
		)


		# emplacementFichierAuditFile
		self.emplacementFichierAuditFile_label = ttk.Label(
			self.tab1_frame1, 
			text = ba_app_var['param']['init']['emplacementFichierAuditFile']['label']
		)
		self.emplacementFichierAuditFile_label.grid(
			row = 2, 
			column = 0, 
			sticky = "e"
		)

		self.emplacementFichierAuditFile_Entry = ttk.Entry(
			self.tab1_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['emplacementFichierAuditFile']['value']
		)
		self.emplacementFichierAuditFile_Entry.grid(
			row = 2, 
			column = 1, 
			sticky = "we"
		)
		self.emplacementFichierAuditFile_Entry.xview_moveto(1)

		self.emplacementFichierAuditFile_Button = ttk.Button(
			self.tab1_frame1, 
			text = 'Parcourir...',
			command = lambda : (
				self.select_savefile(
					parent,
					os.path.dirname(ba_app_var['param']['init']['emplacementFichierAuditFile']['value']),
					[("Fichier CSV", ".csv"), ("All files", ".*")],
					'fichier_audit',
					'.csv',
					'emplacementFichierAuditFile'
				)
			)
		)
		self.emplacementFichierAuditFile_Button.grid(
			row = 2,
			column = 2,
			sticky = "w"
		)


		# Ajout de marges
		for child in self.tab1_frame1.winfo_children(): 
			child.grid_configure(padx = 5, pady = 5)


		# Cadre 2
		self.tab1_frame2 = ttk.Frame(self.tab1)
		self.tab1_frame2.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = (30, 10)
		)
		self.tab1_frame2.rowconfigure(0, weight = 1)
		self.tab1_frame2.columnconfigure(0, weight = 1)


		# Lancement du traitement
		self.run_Button_auditFile = ttk.Button(
			self.tab1_frame2, 
			text = 'Auditer les fichiers',
			style = "Accent.TButton"
		)
		self.run_Button_auditFile.grid(
			row = 0,
			column = 0,
			sticky = "s"
		)


		# Message d'erreur
		self.msg_auditFile = ttk.Label(
			self.tab1_frame2,
			text='',
			justify="center",
			font=("-size", 8),
		)
		self.msg_auditFile.grid(
			row = 1,
			column = 0,
			sticky = "s",
			pady = (10, 0)
		)






		# Onglet 2
		self.tab2 = ttk.Frame(self.notebook)
		self.tab2.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = (20, 0)
		)

		self.notebook.add(
			self.tab2, 
			text="Audit PostgreSQL"
		)


		# Cadre 1
		self.tab2_frame1 = ttk.Frame(self.tab2)
		self.tab2_frame1.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = 0
		)
		self.tab2_frame1.columnconfigure(0, weight = 1)
		self.tab2_frame1.columnconfigure(1, weight = 5)
		self.tab2_frame1.columnconfigure(2, weight = 1)


		# connexionString
		self.connexionString_label = ttk.Label(
			self.tab2_frame1, 
			text = "Ligne de connexion PostgreSQL"
		)
		self.connexionString_label.grid(
			row = 0, 
			column = 0, 
			sticky = "e"
		)

		self.connexionString_Entry = ttk.Entry(
			self.tab2_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['connexionString']['value']
		)
		self.connexionString_Entry.grid(
			row = 0, 
			column = 1, 
			sticky = "we"
		)
		self.connexionString_Entry.xview_moveto(1)


		# schemaDataOfAudit
		self.schemaDataOfAudit_label = ttk.Label(
			self.tab2_frame1, 
			text = ba_app_var['param']['init']['schemaDataOfAudit']['label']
		)
		self.schemaDataOfAudit_label.grid(
			row = 1, 
			column = 0, 
			sticky = "e"
		)

		self.schemaDataOfAudit_Entry = ttk.Entry(
			self.tab2_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['schemaDataOfAudit']['value']
		)
		self.schemaDataOfAudit_Entry.grid(
			row = 1, 
			column = 1, 
			sticky = "we"
		)
		self.schemaDataOfAudit_Entry.xview_moveto(1)


		# schemaDataToAudit
		self.schemaDataToAudit_label = ttk.Label(
			self.tab2_frame1, 
			text = ba_app_var['param']['init']['schemaDataToAudit']['label']
		)
		self.schemaDataToAudit_label.grid(
			row = 2, 
			column = 0, 
			sticky = "e"
		)

		self.schemaDataToAudit_Entry = ttk.Entry(
			self.tab2_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['schemaDataToAudit']['value']
		)
		self.schemaDataToAudit_Entry.grid(
			row = 2, 
			column = 1, 
			sticky = "we"
		)
		self.schemaDataToAudit_Entry.xview_moveto(1)


		# emplacementFichierAuditBDD
		self.emplacementFichierAuditBDD_label = ttk.Label(
			self.tab2_frame1, 
			text = ba_app_var['param']['init']['emplacementFichierAuditBDD']['label']
		)
		self.emplacementFichierAuditBDD_label.grid(
			row = 3, 
			column = 0, 
			sticky = "e"
		)

		self.emplacementFichierAuditBDD_Entry = ttk.Entry(
			self.tab2_frame1, 
			width = 50, 
			textvariable = ba_app_var['param']['init_tk']['emplacementFichierAuditBDD']['value']
		)
		self.emplacementFichierAuditBDD_Entry.grid(
			row = 3, 
			column = 1, 
			sticky = "we"
		)
		self.emplacementFichierAuditBDD_Entry.xview_moveto(1)

		self.emplacementFichierAuditBDD_Button = ttk.Button(
			self.tab2_frame1, 
			text = 'Parcourir...',
			command = lambda : (
				self.select_dir(
					parent,
					os.path.dirname(ba_app_var['param']['init']['emplacementFichierAuditBDD']['value']),
					'emplacementFichierAuditBDD'
				)
			)
		)
		self.emplacementFichierAuditBDD_Button.grid(
			row = 3,
			column = 2,
			sticky = "w"
		)


		# Ajout de marges
		for child in self.tab2_frame1.winfo_children(): 
			child.grid_configure(padx = 5, pady = 5)


		# Cadre 2
		self.tab2_frame2 = ttk.Frame(self.tab2)
		self.tab2_frame2.pack(
			fill = "both", 
			expand = True,
			padx = 0,
			pady = (30, 10)
		)
		self.tab2_frame2.rowconfigure(0, weight = 1)
		self.tab2_frame2.columnconfigure(0, weight = 1)


		# Lancement du traitement
		self.run_Button_auditBDD = ttk.Button(
			self.tab2_frame2, 
			text = 'Auditer la BDD',
			style = "Accent.TButton"
		)
		self.run_Button_auditBDD.grid(
			row = 0,
			column = 0,
			sticky = "s"
		)


		# Message d'erreur
		self.msg_auditBDD = ttk.Label(
			self.tab2_frame2,
			text='',
			justify="center",
			font=("-size", 8),
		)
		self.msg_auditBDD.grid(
			row = 1,
			column = 0,
			sticky = "s",
			pady = (10, 0)
		)






	# Fonction de sélection d'un répertoire
	def select_dir(self, parent, initial_dir, variable):

		dirname = fd.askdirectory(
			title = 'Choisir un répertoire',
			initialdir = initial_dir
		)

		# Définition de la variable
		ba_app_var['param']['init_tk'][variable]['value'].set(dirname)

		# Modification de la vue
		getattr(self, variable + '_Entry').xview_moveto(1)



	# Fonction de sélection d'un fichier existant
	def select_openfile(self, parent, initial_dir, types_fichier, variable):

		filename = fd.askopenfilename(
			title = "Choisir un fichier",
			initialdir = initial_dir,
			filetypes = types_fichier,
		)

		# Définition de la variable
		ba_app_var['param']['init_tk'][variable]['value'].set(filename)

		# Modification de la vue
		getattr(self, variable + '_Entry').xview_moveto(1)



	# Fonction de sélection d'un fichier à créer
	def select_savefile(self, parent, initial_dir, types_fichier, nom_initial, extension_defaut, variable):

		filename = fd.asksaveasfilename(
			title = "Choisir un fichier",
			initialdir = initial_dir,
			initialfile = nom_initial,
			defaultextension = extension_defaut,
			filetypes = types_fichier,
		)

		# Définition de la variable
		ba_app_var['param']['init_tk'][variable]['value'].set(filename)

		# Modification de la vue
		getattr(self, variable + '_Entry').xview_moveto(1)

