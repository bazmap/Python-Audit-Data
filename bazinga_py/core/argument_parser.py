# -*-coding:Utf-8 -*

# Gestion des arguments
# Le contenu ne doit pas changer

# Modules requis
import argparse



# Fonction de gestion des arguments
def argumentParser(software_info, config_var_default):

	# Création d'un parser
	parser = argparse.ArgumentParser(
		description = 
			software_info['name'] + '\n' + 
			"Version : " + software_info['version'] + '\n' + 
			software_info['resume'],
		epilog = 
			"Merci d'utiliser ce programme" + '\n' + 
			software_info['author'] + " - " + software_info['copyright'],
		formatter_class=argparse.RawTextHelpFormatter
	)



	# Définition des arguments
	for key in config_var_default:

		# Récupération de la valeur par défaut pour l'argument
		if 'default_user' in config_var_default[key]:
			default_arg = str(config_var_default[key]['value_user'] or 'None')
		else:
			default_arg = str(config_var_default[key]['value'] or 'None')

		# Définition de l'action
		if config_var_default[key]['type'] == 'boolean':
			action_arg = 'store_const'
			const_arg = not config_var_default[key]['value']
		else:
			action_arg = 'store'
			const_arg = None

		# Suppression de l'aide pour certains arguments
		# L'argument est donc toujours disponible si besoin
		if 'argument' in config_var_default[key]['input_scope']:
			help_arg = config_var_default[key]['help'] + ' \nValeur attendue : ' + config_var_default[key]['type'] + ' - ' + config_var_default[key]['expected'] + '\nValeur par défaut : ' + default_arg
		else:
			help_arg = argparse.SUPPRESS

		# Ajout des arguments
		parser.add_argument(
			'--' + key,
			action = action_arg,
			const = const_arg,
			default = config_var_default[key]['value'],
			help = help_arg
		)

	parser.add_argument(
		'--version', '-v',
		action = 'version',
		version = software_info['name'] + ' - v' + software_info['version'],
		help = "Version du script"
	)



	# Récupération des variables à utiliser
	variables = dict()

	for key, value in vars(parser.parse_args()).items():
		variables[key] = {
			'value' : value
		}

	return variables