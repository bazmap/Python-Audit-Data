# -*-coding:Utf-8 -*

# Définition des paramètres du programme
# La structure doit rester identique, seules les valeurs des variables change
# Le but est ici décraser des valeurs prédéfinies dans certains variables et d'en ajouter d'autres au besoin

# Modules requis
import os
import datetime

from bazinga_py.core.config_default import app_var



# Software
app_var['software']['name'] = "Audit de données"
app_var['software']['version'] = "1.3"
app_var['software']['resume'] = "Programme d'audit automatisé des données spatiales"
app_var['software']['author'] = "Arthur Bazin"
app_var['software']['copyright'] = datetime.datetime.now().strftime("%Y") + " - Arthur Bazin"
#app_var['software']['dir'] = ""
#app_var['config_dir']['config_dir'] = os.path.join(app_var['software']['dir'], 'config')
#app_var['config_dir']['config_file_default'] = 'default.conf'
#app_var['software']['logo'] = os.path.normpath(os.path.join(app_var['software']['dir'], 'media\\software_icon.gif'), )
#app_var['software']['icon'] = os.path.normpath(os.path.join(app_var['software']['dir'], 'media\\software_icon.gif'), )
app_var['software']['splash_screen'] = os.path.normpath(os.path.join(app_var['software']['dir'], 'media\\software_splash_screen.gif'), )
app_var['software']['size']['x'] = 1000
app_var['software']['size']['y'] = 600



# Logs
#app_var['log']['dir'] = os.path.join(app_var['software']['dir'], 'logs'),
#app_var['log']['name'] = 'Log' + "_" + app_var['execution_date'].strftime("%Y-%m-%d_%H-%M-%S") + ".log",
#app_var['log']['prefix_to_delete'] = 'Log',
#app_var['log']['type'] = 'simple',
#app_var['log']['nb_to_keep'] = 3,
#app_var['log']['min_level'] = 'DEBUG',
#app_var['log']['stdout_levels'] = ['DEBUG']



# Initialisation des variables de configuration et d'arguments
app_var['param']['config_framework'] = {
	'emplacementDataAnalyse': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : app_var['software']['dir'],
		'value_user' : None,
		'expected': 'Chemin absolu vers un répertoire',
		'group': 'Emplacement',
		'label': "Répertoire à auditer",
		'help' : "Répertoire dont le contenu doit être audité."
	},
	'emplacementFichierAuditFile': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : os.path.join(
			app_var['software']['dir'], 
			'Audit',
			'Audit Fichier.csv'
		),
		'value_user' : None,
		'expected': 'Chemin absolu vers un fichier',
		'group': 'Emplacement',
		'label': "Fichier de résultat d'audit",
		'help' : "Le résultat de l'audit est par défaut stocké dans un fichier csv nommé 'Audit Fichier.csv' et créé dans le répertoire 'Audit' de ce programme. Cette option permet de modifier le nom et l'emplacement du fichier."
	},
	'connexionString': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : 'postgresql://postgres:postgres@127.0.0.1:5432/postgres',
		'expected': 'URI : postgresql://[user[:password]@][host][:port][/dbname]',
		'group': 'BDD Destination',
		'label': "BDD PostgreSQL à auditer",
		'help' : "Ligne de connexion à la base de données PostgreSQL à auditer."
	},
	'schemaDataOfAudit': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : 'audit_data',
		'expected': 'nom_schema',
		'group': 'BDD Destination',
		'label': "Schéma contenant les données d'audit",
		'help' : "Nom du schéma contenant les données d'audit"
	},
	'schemaDataToAudit': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : 'mon_schema1,nom_schema2',
		'expected': 'nom_schema1,nom_schema2...',
		'group': 'BDD Destination',
		'label': "Schémas à auditer",
		'help' : "Nom des schémas à auditer"
	},
	'emplacementFichierAuditBDD': {
		'input_scope' : ['argument','config'],
		'type' : 'string',
		'value' : os.path.join(
			app_var['software']['dir'], 
			'Audit'
		),
		'value_user' : None,
		'expected': 'Chemin absolu vers un répertoire',
		'group': 'Emplacement',
		'label': "Emplacement des fichiers d'audit",
		'help' : "Le résultat de l'audit est par défaut stocké dans plusieurs fichiers csv dans le répertoire 'Audit' de ce programme. Cette option permet de modifier l'emplacement des fichiers."
	}
}



#######################
# Variables spécifiques
#######################

# Formats spatiaux
app_var['var']['format_specifique'] = {
	"Vecteur spatial" : [
		'shp',
		'mif',
		'mid',
		'dxf',
		'dwg',
		'mdb',
		'thf',
		'bna',
		'gpx',
		'geojson',
		'kml',
		'kmz',
		'mbtiles',
		'dgn',
		'gdb',
		'gpkg',
		'pbf',
		'osm',
		'mvt',
		'mvt.gz'
	],
	"Backup BDD" : [
		'dump',
		'backup',
		'dmp'
	],
	"Alphanumeric" : [
		'dbf',
		'tab',
		'xls',
		'xlsx',
		'xlsm',
		'db',
		'db3',
		'sqlite',
		'sqlite3',
		'csv',
		'json',
		'xml'
	],
	"Raster" : [
		'ecw',
		'tif',
		'tiff',
		'jp2',
		'j2k',
		'xyz',
		'asc',
		'grd',
		'dem',
		'vrt'
	],
	"Projet FME" : [
		'fmw'
	],
	"Projet QGIS" : [
		'qgs',
		'qgz'
	],
	"Projet ArcGIS" : [
		'aprx'
	],
	"Document" : [
		'pdf',
		'doc',
		'docx',
		'rtf',
		'md',
		'txt'
	]
}


# Formats supportés pour l'import
app_var['var']['supported_import_format'] = dict(
	csv = '-oo HEADERS=YES -oo EMPTY_STRING_AS_NULL=YES',
	shp = '-lco GEOMETRY_NAME=geom'
)


