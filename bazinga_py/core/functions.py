# -*-coding:Utf-8 -*

# Fonctions standard du framework
# Le contenu ne doit pas changer

# Modules requis
import os
import copy
import json
import tkinter as tk
import random



# Fonction de coalesce
def coalesce(*args):
	for arg in args:
		if arg is not None:
			return arg
	
	return None



# Fonction d'affichage des dictionnaires
def dprint(my_dict, prefix = ''):

	for key, value in my_dict.items():

		if isinstance(value, dict):
			print(prefix + key + ' ' + str(type(value)) + ': ')
			dprint(value, prefix + '	')

		else:
			print(prefix + key + ' ' + str(type(value)) + ': ' + str(value))

	return None



# Fonction de récupération des variables de configuration
def getConfigVar(standard_config, var_configFile, var_args):

	# Ordre de récupération des variables :
		# Valeur par défaut
		# Valeur fichier de config
		# Valeur de l'argument

	# Initialisation de la valeur par copie de la configuration standard
	final_config = copy.deepcopy(standard_config)



	# Récupération des valeurs du fichier de config
	# On récupère aussi les variables supplémentaires définies dans le fichier mais non prévues par défaut.
	if var_configFile != None:
		for key in var_configFile:
			if key not in final_config:
				final_config[key] = dict()

			if 'value' not in final_config[key]:
				final_config[key]['group'] = var_configFile[key]['group']

			final_config[key]['value'] = var_configFile[key]['value']

			if 'scope' not in final_config[key]:
				final_config[key]['scope'] = ['config']
			elif 'config' not in final_config[key]['scope']:
				final_config[key]['scope'].append('config')



	# Récupération des valeurs des arguments
	for key in var_args:

		if standard_config[key]['value'] != var_args[key]['value']:
			final_config[key]['value'] = var_args[key]['value']



	return final_config



# Fonction de vérification de la présence d'une police
def checkFontAvailability(*fontName):

	# Mise à jour de l'affichage
	for checkedFont in fontName:

		if checkedFont in tk.font.families():

			return checkedFont
	
	# Renvoi d'une font par défaut
	return tk.font.nametofont("TkDefaultFont").actual()['family']



# Fonction de défilement d'un widget avec la molette de la souris
def set_mousewheel(widget):
	"""Activate / deactivate mousewheel scrolling when 
	cursor is over / not over the widget respectively."""
	widget.bind(
		"<Enter>", 
		lambda _: widget.bind_all(
			'<MouseWheel>', 
			lambda event: widget.yview_scroll(
				int(-1*(event.delta/120)),
				"units"
			)
		)
	)
	widget.bind(
		"<Leave>", 
		lambda _: widget.unbind_all(
			'<MouseWheel>'
		)
	)



# Suprise me
def surpriseMe():
	message = dict()

	message[1] ="""
                 AB                    ABABABABABABABABABAB
                ABAB                   ABABABABABABABABABABAB
              ABABABAB                 ABAB              ABAB
            ABAB    ABAB               ABAB              ABAB
          ABAB        ABAB             ABABABABABABABABABAB
        ABAB            ABAB           ABABABABABABABABABAB
      ABAB                ABAB         ABAB              ABAB
    ABAB                   ABAB        ABAB              ABAB
  ABAB     ABABABABABABABABABABAB      ABABABABABABABABABABAB
ABAB    ABABABABABABABABABABABABABA    ABABABABABABABABABAB
"""

	message[2] ="""
BGBG    BGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG        
BGBG    BGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG        
BGBG                                                                        
BGBG                                                                        
BGBG    BGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBG    BGBG    BGBG        
BGBG    BGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBG    BGBG    BGBG        
BGBG            BGBG                            BGBG            BGBG        
BGBG            BGBG                            BGBG            BGBG        
BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBG
BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBGBGBGBGBGBGBGBGBG    BGBG
"""

	return message[random.randint(1, 2)]
	




# Fonction d'affichage d'un fichier de configuration
def retrieveConfigFile(config_var, default = True):

	config_file_content = """# Fichier de configuration

# L'argument "--configFile" permet d'utiliser un autre fichier de configuration
# Les valeurs passées en argument auront la priorité sur les valeurs définie dans ce fichier."""



	# Liste des groupes
	group_list = []
	for key in config_var:

		if config_var[key]['group'] not in group_list:
			group_list.append(config_var[key]['group'])



	for group in group_list:

		config_file_content += '\n\n\n'
		config_file_content += '[' + group + ']'

		for key in config_var:

			if (
				config_var[key]['group'] == group 
				and 'input_scope' in config_var[key]
				and 'config' in config_var[key]['input_scope']
			):

				config_file_content += '\n\n'
				config_file_content += key + '=' 

				if default == True:
					if 'default_user' in config_var[key]:
						config_file_content += str(config_var[key]['value_user'] or 'None')
					
					else:
						config_file_content += str(config_var[key]['value'] or 'None')
				
				else:
					config_file_content += str(config_var[key]['value'] or 'None')

				config_file_content += '\n' + '# ' + config_var[key]['help'].replace("\n", "\n# ")
				config_file_content += '\n' + '# Valeur attendue : ' + config_var[key]['type'] + ' - ' + str(config_var[key]['expected'])
		
	return config_file_content



# Fonction de chargement d'un fichier json
def jsonLoader(file_path):

	var_config = None

	if os.path.exists(file_path):

		with open(file_path, 'r') as config_file:
			var_config = json.load(config_file)

	return var_config