# -*-coding:Utf-8 -*

# Programme d'audit des fichiers

# Modules requis
import os
import csv
import datetime

from bazinga_py.init import *
import core.functions as functions



##############################################################
# Programme 
##############################################################

# Programme d'audit des fichiers
def auditFile(
	app, 
	rootWindows
):

	function_start_date = datetime.datetime.now()

	ba_logger.info("Fonction auditFile")
	ba_logger.info("Liste des variables :")
	ba_logger.info("	" + "emplacementDataAnalyse = " + ba_app_var['param']['init_tk']['emplacementDataAnalyse']['value'].get())
	ba_logger.info("	" + "emplacementFichierAuditFile = " + ba_app_var['param']['init_tk']['emplacementFichierAuditFile']['value'].get())


	# Désactivation du bouton
	app.run_Button_auditFile["state"] = "disabled"


	# Affichage d'un message
	app.msg_auditFile['text'] = "Traitement en cours..."
	rootWindows.update()


	# Listing des fichiers
	######################
	ba_logger.info("Listing des fichier")
	ba_logger.info("Emplacement du fichier d'audit : " + ba_app_var['param']['init_tk']['emplacementFichierAuditFile']['value'].get())


	try:

		ba_logger.info("Création du fichier d'audit")

		# Ouverture du fichier CSV en mode écriture
		with open(ba_app_var['param']['init_tk']['emplacementFichierAuditFile']['value'].get(), mode='w', newline='') as fichier_csv:

			# Création d'un objet writer
			writer = csv.writer(
				fichier_csv, 
				delimiter=';', 
				quotechar='"', 
				quoting=csv.QUOTE_MINIMAL
			)



			ba_logger.info("Création de la première ligne")

			# Écriture de l'en-tête du fichier CSV
			writer.writerow(
				[
					'Nom', 
					'Extension',
					'Nom complet',
					'Type donnees',
					'Chemin complet', 
					'Taille (octets)', 
					'Taille (lisible)', 
					'Date de création', 
					'Date de modification'
				]
			)



			# Parcourt des sous-répertoires et des fichiers du répertoire
			ba_logger.info("Parcours des fichiers")
			for repertoire_actuel, sous_repertoires, fichiers in os.walk(ba_app_var['param']['init_tk']['emplacementDataAnalyse']['value'].get()):

				# Parcourt la liste des fichiers et affiche les attributs de chaque fichier
				for fichier in fichiers:

					# Chemin complet du fichier
					chemin_fichier = os.path.join(repertoire_actuel, fichier)

					format_donnees = 'Autre'

					for type_donnee in ba_app_var['var']['format_specifique']:

						if ((os.path.splitext(fichier)[1])[1:]).lower() in ba_app_var['var']['format_specifique'][type_donnee]:
							format_donnees = type_donnee

					# Écriture des informations dans le fichier
					writer.writerow(
						[
							os.path.splitext(fichier)[0], 
							((os.path.splitext(fichier)[1])[1:]).lower(),
							fichier,
							format_donnees,
							chemin_fichier, 
							str(os.path.getsize(chemin_fichier)), 
							functions.taille_lisible(os.path.getsize(chemin_fichier)), 
							datetime.datetime.fromtimestamp(os.path.getctime(chemin_fichier)).strftime("%Y-%m-%d %H:%M:%S"), 
							datetime.datetime.fromtimestamp(os.path.getmtime(chemin_fichier)).strftime("%Y-%m-%d %H:%M:%S")
						]
					)


	except Exception as err:
		ba_logger.info("Erreur de traitement : " + str(err))

		app.msg_auditFile['text'] = "Erreur de traitement : " + str(err)
		rootWindows.update()

	else:
		ba_logger.info("Traitement terminé")

		app.msg_auditFile['text'] = "Traitement terminé"
		rootWindows.update()


	# Réactivation du bouton
	app.run_Button_auditFile["state"] = "enable"


	# Fin du traitement
	ba_logger.info('Temps de traitement : ' + str(datetime.datetime.now() - function_start_date ))


