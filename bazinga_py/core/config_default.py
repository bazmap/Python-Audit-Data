# -*-coding:Utf-8 -*

# Variables standard du framework
# Le contenu ne doit pas changer

# Modules requis
import os
import datetime
import inspect



# Initialisation de la variable principale de paramètrage
app_var = dict()



# Initialisation timestamp démarrage
app_var['execution_date'] = datetime.datetime.now()



# Récupération de la stack
fileStack = []
if __name__ != '__main__':
	for frame in inspect.stack()[1:]:
		if frame.filename[0] != '<':
			fileStack.append(frame.filename)



# Framework
app_var['framework'] = dict(
	name = "bazinga_py",
	version = "1.0",
	dir = os.path.join(os.path.dirname(__file__), '..\\')
)



# Software
app_var['software'] = dict(
	name = os.path.splitext(os.path.basename(fileStack[-1]))[0],
	version = "0.0",
	resume = "",
	author = "",
	copyright = datetime.datetime.now().strftime("%Y") + "",
	dir = os.path.dirname(fileStack[-1]),
	config_dir = os.path.join(
		os.path.dirname(fileStack[-1]), 
		'config'
	),
	config_file_default = 'default.conf',
	logo = os.path.normpath(os.path.join(app_var['framework']['dir'], 'media\\software_icon.gif'), ),
	icon = os.path.normpath(os.path.join(app_var['framework']['dir'], 'media\\software_icon.gif'), ),
	splash_screen = os.path.normpath(os.path.join(app_var['framework']['dir'], 'media\\software_splash_screen.gif'), )
)



# Logs
app_var['log'] = dict(
	dir = os.path.join(app_var['software']['dir'], 'logs'),
	name = 'Log' + "_" + app_var['execution_date'].strftime("%Y-%m-%d_%H-%M-%S") + ".log",
	prefix_to_delete = 'Log',
	type = 'simple',
	nb_to_keep = 10,
	min_level = 'DEBUG',
	stdout_levels = ['DEBUG']
)



# Initialisation des variables de configuration et d'arguments
app_var['param'] = dict()

app_var['param']['framework'] = {
	'configFile': {
		'input_scope' : ['argument'],
		'type' : 'string',
		'value' : app_var['software']['config_file_default'],
		'value_user' : None,
		'expected': 'Nom d\'un fichier en ".conf"',
		'group': 'Général',
		'help' : "Nom du fichier de configuration à utiliser. Les valeurs passées en argument seront utilisées à la place de celles spécifiées dans le fichier de configuration."
	},
	'printConfigFile': {
		'input_scope' : ['argument'],
		'type' : 'boolean',
		'value' : False,
		'expected': 'True/False',
		'group': 'Général',
		'help' : "Affichage d'un fichier de configuration par défaut. Aucun traitement n'est effectué."
	},
	'logFileNumber': {
		'input_scope' : ['argument','config'],
		'type' : 'integer',
		'value' : app_var['log']['nb_to_keep'],
		'expected': 'n',
		'group': 'Log',
		'help' : "Nombre de fichier de log à conserver."
	},
	'surpriseMe': {
		'input_scope' : ['argument'],
		'type' : 'boolean',
		'value' : False,
		'expected': 'True/False',
		'group': 'Général',
		'help' : "A vous de voir."
	}
}



#######################
# Variables spécifiques
#######################

# Liste de variables spécifiques au programme
app_var['var'] = dict()