# -*-coding:Utf-8 -*

# Gestion des fichiers de configuration
# Le contenu ne doit pas changer

# Modules requis
import os
import configparser



# Fonction de chargement d'un fichier de configuration
def configLoader(file_path):

	# Création d'un parser
	parser = configparser.ConfigParser(
		empty_lines_in_values=False,
		interpolation=configparser.ExtendedInterpolation()
	)

	# Ajout des booléens français
	parser.BOOLEAN_STATES.update(
		{
			'oui' : True,
			'Oui' : True,
			'OUI' : True,
			'non' : False,
			'Non' : False,
			'NON' : False
		}
	)

	# Conservation de la casse dans les noms de paramètre
	parser.optionxform = lambda option : option


	var_config = None

	# Lecture du fichier de configuration s'il existe
	if os.path.exists(file_path):
		parser.read(
			file_path,
			encoding='UTF-8'
		)

		var_config = parserVarExtractor(parser)

	# Renvoie des valeurs
	return var_config



# Extraction des variable d'un parser
def parserVarExtractor(parser):

	# Création d'un dictionnaire qui va stocker les valeurs
	variables = dict()

	# Récupération des valeurs de variable
	# Pour chaque section de paramètre
	for group in parser.sections():

		# Pour chaque variable du groupe
		for key in parser.options(group):

			# Récupération des valeurs
			variables[key] = dict(
				value = parser[group][key],
				group = group
			)

	return variables


