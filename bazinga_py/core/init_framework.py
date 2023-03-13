# -*-coding:Utf-8 -*

# Initialisation du framework
# Le contenu ne doit pas changer

# Modules requis
import os
import copy

from bazinga_py.core import config_default
from bazinga_py import config as config_user
from bazinga_py.core import functions
from bazinga_py.core import argument_parser
from bazinga_py.core import config_file_parser
from bazinga_py.core import logger as my_logger



# Récupération des variables de configuration du programme
app_var = copy.deepcopy({**config_default.app_var, **config_user.app_var})

# Récupération des variables de configuration
app_var['param']['software'] = copy.deepcopy({**app_var['param']['framework'], **app_var['param']['config_framework']})



# Définition d'un groupe par défaut
for key in app_var['param']['software']:

	if app_var['param']['software'][key]['group'] == '':
		app_var['param']['software'][key]['group'] = 'Général'



# Initialisation des arguments
app_var['param']['arg'] = argument_parser.argumentParser(
	app_var['software'], 
	app_var['param']['software']
)



# Gestion des actions à mener directement à partir des arguments
if app_var['param']['arg']['printConfigFile']['value'] :
	# Affichage d'un fichier de configuration par défaut
	print(functions.retrieveConfigFile(app_var['param']['software']))
	exit()

if app_var['param']['arg']['surpriseMe']['value'] :
	# Elément de surprise
	print(functions.surpriseMe())
	exit()



# Initialisation des fichiers de configuration
app_var['param']['config_file'] = config_file_parser.configLoader(
	os.path.join(
		app_var['software']['config_dir'],
		functions.coalesce(app_var['param']['arg']['configFile']['value'], app_var['software']['config_file_default'])
	)
)



# Création des variables de configuration par défaut
app_var['param']['init'] = functions.getConfigVar(app_var['param']['software'], app_var['param']['config_file'], app_var['param']['arg'])



# Initialisation du logger
logger = my_logger.createLogger(
	app_var['log']['name'], 
	app_var['log']['dir'], 
	app_var['log']['min_level'], 
	app_var['log']['stdout_levels'], 
	int(app_var['param']['init']['logFileNumber']['value']),
	app_var['log']['prefix_to_delete'], 
	app_var['log']['type']
)

logger.info(app_var['software']['name'] + ' - v' + app_var['software']['version'])
logger.info(app_var['software']['author'] + ' - ' + app_var['software']['copyright'])
logger.info('')