# -*-coding:Utf-8 -*

# Programme principal

# Modules requis
from bazinga_py.init import *

import importlib
import subprocess

import core.auditFile as auditFile
import core.auditBDD as auditBDD
import core.functions as functions
import core.tk_rootInterface as tk_rootInterface



# Initialisation de l'interface graphique
rootWindows = ba_rootWindows()



# Vérification de la présence de psycopg
try:
	importlib.import_module('psycopg')

	ba_logger.info("L\'extension psycopg est installée")

	ba_logger.info("Mise à jour")

	# Commande pour installer psycopg
	command = "pip install --upgrade psycopg"
	ba_logger.info("Mise à jour automatique : " + command)

	# Exécute la commande et capture la sortie
	output = subprocess.check_output(command, shell=True)
	# Affiche la sortie de la commande
	ba_logger.info(output.decode())


except ImportError:

	ba_logger.info("L\'extension psycopg n'est pas installée")

	# Commande pour installer psycopg
	command = "pip install psycopg[binary]"
	ba_logger.info("Installation automatique : " + command)

	# Exécute la commande et capture la sortie
	output = subprocess.check_output(command, shell=True)

	# Affiche la sortie de la commande
	ba_logger.info(output.decode())



# Ajout des widgets à l'interface principale
app = tk_rootInterface.rootInterface(rootWindows)
app.pack(
	fill="both", 
	expand=True,
	padx=0,
	pady=0
)



# Execution de la fonction principale lors du click sur le bouton de lancement
app.run_Button_auditFile.bind(
	'<ButtonPress-1>', 
	lambda event: auditFile.auditFile(
		app = app,
		rootWindows = rootWindows
	)
)



# Execution de la fonction principale lors du click sur le bouton de lancement
app.run_Button_auditBDD.bind(
	'<ButtonPress-1>', 
	lambda event: auditBDD.auditBDD(
		app = app,
		rootWindows = rootWindows
	)
)



# Mise en place de la boucle d'écoute d'évènement
rootWindows.run_mainloop()