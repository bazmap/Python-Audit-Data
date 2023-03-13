# -*-coding:Utf-8 -*

# Import des données

# Modules requis
import os
import subprocess



# Fonction d'import
def import_ogr_pg(
	pg_connexion_string,
	schema_name,
	table_name,
	importmethod,
	data_file,
	specific_args,
	gdal_path,
):

	# Initialisation valeur de retour
	result = dict()


	# Ligne de commande OGR
	ogr_cmd = '"{gdal_path}\\ogr2ogr" -f PostgreSQL "{pg_connexion_string}" {specific_args} -{importmethod} -nln "{schema_name}.{table_name}" "{data_file}"'

	# Incorporation des variables
	ogr_cmd_full = ogr_cmd.format(
		gdal_path = os.path.normpath(gdal_path),
		pg_connexion_string = pg_connexion_string,
		schema_name = schema_name,
		table_name = table_name,
		importmethod = importmethod,
		data_file = os.path.normpath(data_file),
		specific_args = specific_args
	)



	# Définition des variables d'environnement de GDAL
	var_env = os.environ.copy()
	var_env['PROJ_LIB'] = os.path.join(gdal_path + "projlib")
	var_env['GDAL_DRIVER_PATH'] = os.path.join(gdal_path + "gdalplugins")
	var_env['GDAL_DATA'] = os.path.join(gdal_path + "gdal-data")



	# Exécution du sous processus
	proc = subprocess.Popen(
		ogr_cmd_full, 
		shell = True, 
		env = var_env,
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE
	)


	# Communication avec le sous processus
	proc_output, proc_error = proc.communicate()

	# Attente de la fin du processus
	proc.wait()

	# Récupértion du code de retour
	result['returncode'] = proc.returncode


	# Si on a une erreur
	if result['returncode'] != 0:
		result['message'] = "	Erreur lors de l'import \n Message : \n" + str(proc_error)
	
	else:
		output_message = proc_output.decode('UTF-8')
		if output_message != '':
			output_message = "\n Message : \n" + output_message

		result['message'] = "	Import réussi" + output_message

	return result


