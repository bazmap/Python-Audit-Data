# -*-coding:Utf-8 -*

# Gestion des logs
# Le contenu ne doit pas changer

# Modules requis
import logging
import logging.handlers
import os
import re



# Fonction de création d'un logger
def createLogger(log_name, log_directory, min_logging_level = 'DEBUG', stdout_logging_levels = ['DEBUG'], nb_of_log = 10, prefix_to_delete = 'log', logger_type = 'simple'):

	# Instantiation du logger
	logger = logging.getLogger(log_name)

	# Définition du niveau de log
	logger.setLevel(min_logging_level)



	# Log ver la sortie stdout
	if stdout_logging_levels == ['ALL']:
		stdout_logging_levels = ['DEBUG','INFO','WARNING','ERROR','CRITICAL']

	logger.addHandler(createStreamHandler(stdout_logging_levels))

	# Association du logger au gestionnaire
	if logger_type == 'rotating':
		logger.addHandler(createRotatingFileHandler(log_name, log_directory, nb_of_log, prefix_to_delete))
	else:
		logger.addHandler(createFileHandler(log_name, log_directory, nb_of_log, prefix_to_delete))


	# Renvoi du logger
	return logger



# Fonction de création d'un gestionnaire de log
def createRotatingFileHandler(log_name, log_directory, nb_of_log = 10, prefix_to_delete = 'log'):

	# Suppression des anciens logs
	limitFileNumber(log_directory, (nb_of_log - 1), prefix_to_delete)


	# Définition d'un gestionnaire
	handler = logging.handlers.RotatingFileHandler(
		filename = os.path.join(log_directory, log_name),
		maxBytes = 2000000, 
		backupCount = nb_of_log,
		encoding = 'utf-8'
	)


	# Formatage des messages
	formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")	
	handler.setFormatter(formatter)

	return handler



# Fonction de création d'un gestionnaire de log
def createFileHandler(log_name, log_directory, nb_of_log = 10, prefix_to_delete = 'log'):

	# Suppression des anciens logs
	limitFileNumber(log_directory, (nb_of_log - 1), prefix_to_delete)


	# Définition d'un gestionnaire
	handler = logging.FileHandler(
		filename = os.path.join(log_directory, log_name),
		encoding = 'utf-8'
	)


	# Formatage des messages
	formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")	
	handler.setFormatter(formatter)

	return handler



def createStreamHandler(loggin_levels = ['DEBUG']):

	# Définition d'un gestionnaire
	handler = logging.StreamHandler()


	# Formatage des messages
	formatter = logging.Formatter("%(levelname)s | %(message)s")	
	handler.setFormatter(formatter)


	# Définition d'un filtre
	class MyFilter(logging.Filter):
		def __init__(self, loggin_levels):
			self.loggin_levels = loggin_levels

		def filter(self, record):
			return record.levelname in self.loggin_levels

	handler.addFilter(MyFilter(loggin_levels))

	# Renvoi du gestionnaire
	return handler



# Fonction de nettoyage de fichiers
def limitFileNumber(path_directory, max_nb_file = 10, file_prefix = 'log_'):

	# Liste des fichiers situés dans le répertoire
	file_list = filter(
		lambda x: os.path.isfile(
			os.path.join(
				path_directory, 
				x
			)
		),
		os.listdir(path_directory)
	)

	# On ne garde que les fichiers avec le prefixe qui nous intéresse
	file_list = filter(
		lambda x: bool(
			re.search(
				"^" + file_prefix + ".*", 
				x
			)
		),
		file_list
	)

	# Tri des fichier basé sur leur date de dernière modification
	file_list = sorted(
		file_list,
		key = lambda x: os.path.getmtime(
			os.path.join(
				path_directory, 
				x
			)
		),
		reverse = True
	)


	# Numéro d'itération
	i = 0

	# Pour chaque fichier
	for file_name in file_list:

		# On numérote le fichier
		i += 1

		# Si le numéro de fichier est supérieur à ce qui a été prévu, on le supprime
		if i > max_nb_file:

			os.remove( 
				os.path.join(
					path_directory, 
					file_name
				)
			)


