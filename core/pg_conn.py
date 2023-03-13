# -*-coding:Utf-8 -*

# Gestion des connexion PG

# Modules requis
import os
import psycopg



# Fonction de requêtage
def exec_request(sql_request, connexionString):

	# Initialisation connexion BDD dans un contexte
	with psycopg.connect(
		conninfo = connexionString,
		autocommit = True
	) as pg_conn:

		# Définition d'un curseur
		pg_cur = pg_conn.cursor()

		# Exécution requête
		try:
			pg_cur.execute(sql_request)

		except Exception as exception:
			message = "Transaction annulée\n" + str(exception)
			level = 'WARNING'

		else:
			message = pg_cur.statusmessage
			level = 'INFO'


		# Renvoi du message
		return dict(
			level = level, 
			message = message
		)



# Fonction de requêtage à partir d'un fichier
def exec_requestFromFile(request_file_path, connexionString):

	return_msg = dict()

	# Test de l'existance du fichier de requêtage
	if request_file_path != '' and os.path.exists(request_file_path):

		# Lecture du fichier
		with open(request_file_path, "r", encoding="utf-8") as request_file:

			# Exécution des requêtes
			return_msg = exec_request(
				request_file.read(), 
				connexionString
			)

	else:
		return_msg['message'] = 'Le fichier fournit n\'existe pas'
		return_msg['level'] = 'WARNING'

	return return_msg

