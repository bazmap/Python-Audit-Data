# -*-coding:Utf-8 -*

# Programme d'audit des BDD

# Modules requis
import os
import re
import pathlib
import datetime
import psycopg

from bazinga_py.init import *
import core.functions as functions
import core.pg_conn as pg_conn



##############################################################
# Programme 
##############################################################

# Programme d'audit de BDD
def auditBDD(
	app, 
	rootWindows
):

	function_start_date = datetime.datetime.now()

	ba_logger.info("Fonction auditBDD")
	ba_logger.info("Liste des variables :")
	ba_logger.info("	" + "schemaDataOfAudit = " + ba_app_var['param']['init_tk']['schemaDataOfAudit']['value'].get())
	ba_logger.info("	" + "schemaDataToAudit = " + ba_app_var['param']['init_tk']['schemaDataToAudit']['value'].get())
	ba_logger.info("	" + "emplacementFichierAuditBDD = " + ba_app_var['param']['init_tk']['emplacementFichierAuditBDD']['value'].get())


	# Désactivation du bouton
	app.run_Button_auditBDD["state"] = "disabled"


	# Affichage d'un message
	app.msg_auditBDD['text'] = "Traitement en cours..."
	rootWindows.update()


	try:
		ba_logger.info("Traitement en cours")

		SQLFile_directory = os.path.join(
			ba_app_var['software']['dir'],
			'sql'
		)

		# Pour chaque fichier à traiter
		for data_file in os.listdir(SQLFile_directory):

			# On ne garde que les fichier avec la bonne extension
			file_search = re.search(
				".*\.sql", 
				data_file
			)

			# Si le fichier n'a pas la bonne extension, on passe
			if file_search is None:
				continue

			ba_logger.info('=> Fichier : ' + data_file)

			# Lecture du fichier
			with open(
				os.path.join(SQLFile_directory, data_file),
				"r",
				encoding="utf-8"
			) as request_file:

				ba_logger.info('Remplacement des variables')

				sql_text = functions.placeholder_replace(
					request_file.read(),
					'\$\{([a-zA-Z0-9_\-]*)\}',
					{
						"schemaDataOfAudit": ba_app_var['param']['init_tk']['schemaDataOfAudit']['value'].get(),
						"schemaDataToAudit": ba_app_var['param']['init_tk']['schemaDataToAudit']['value'].get()
					}
				)

				# Execution SQL
				###############
				ba_logger.info('	Execution du fichier SQL')

				# Exécution des requêtes
				return_msg = pg_conn.exec_request(
					sql_text, 
					ba_app_var['param']['init_tk']['connexionString']['value'].get()
				)

				if return_msg['level'] == 'WARNING':
					ba_logger.warning(return_msg['message'])
				else:
					ba_logger.info(return_msg['message'])

				ba_logger.info('	Execution terminé')



		# Récupération des données
		ba_logger.info('Récupération des données')

		auditBDDcsvFiles = {
			"bdd" : "audit_bdd",
			"colonne" : "audit_colonne",
			"extension" : "audit_extension",
			"fonction" : "audit_fonction",
			"index" : "audit_index",
			"role" : "audit_role",
			"schema" : "audit_schema",
			"sequence" : "audit_sequence",
			"table" : "audit_table",
			"trigger" : "audit_trigger",
			"valeur" : "audit_valeur",
			"vue" : "audit_vue",
			"vue_materialisee" : "audit_vue_materialisee",
			"table_colonne_valeur" : "audit_table_colonne_valeur",
			"geometrie" : "audit_geometrie"
		}
		for auditBDDcsvFile, auditBDDTable in auditBDDcsvFiles.items():

			ba_logger.info('	Fichier : ' + "Audit BDD - " + auditBDDcsvFile + ".csv")

			with open(
				os.path.join(
					ba_app_var['param']['init_tk']['emplacementFichierAuditBDD']['value'].get(),
					"Audit BDD - " + auditBDDcsvFile + ".csv"),
				"wb"
			) as csvFile:

				# Initialisation connexion BDD dans un contexte
				with psycopg.connect(
					conninfo = ba_app_var['param']['init_tk']['connexionString']['value'].get(),
					autocommit = True
				) as pg_connex:

					# Définition d'un curseur
					pg_cur = pg_connex.cursor()

					# Définition de la requête
					pg_query = psycopg.sql.SQL(
						"COPY (SELECT * FROM {schema}.{table}) TO STDOUT DELIMITER ';' CSV HEADER"
					).format(
						schema=psycopg.sql.Identifier(
							ba_app_var['param']['init_tk']['schemaDataOfAudit']['value'].get()
						),
						table=psycopg.sql.Identifier(
							auditBDDTable
						)
					)

					ba_logger.info('	Démarrage transfert')

					with pg_cur.copy(pg_query) as pg_copy:
						for my_data in pg_copy:
							csvFile.write(my_data)

					ba_logger.info('	Transfert terminé')


	except Exception as err:
		ba_logger.info("Erreur de traitement : " + str(err))

		app.msg_auditBDD['text'] = "Erreur de traitement : " + str(err)
		rootWindows.update()

	else:
		ba_logger.info("Traitement terminé")

		app.msg_auditBDD['text'] = "Traitement terminé"
		rootWindows.update()


	# Réactivation du bouton
	app.run_Button_auditBDD["state"] = "enable"


	# Fin du traitement
	ba_logger.info('Temps de traitement : ' + str(datetime.datetime.now() - function_start_date ))