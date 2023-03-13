# -*-coding:Utf-8 -*

# Fonctions spécifiques du programme

# Modules requis
import re



# Fonction d'affichage des tailles de façon lisible
def taille_lisible(taille_octets):

	# Liste des unités avec leurs tailles correspondantes
	unite_taille = [
		(1024 ** 4, 'To'), 
		(1024 ** 3, 'Go'), 
		(1024 ** 2, 'Mo'), 
		(1024 ** 1, 'ko'), 
		(1, 'o')
	]
	
	# Parcourt des unités de la plus grande à la plus petite
	for taille, unite in unite_taille:
		# Si la taille est supérieure ou égale à l'unité actuelle, calcule la taille dans cette unité
		if taille_octets >= taille:
			taille_lisible = taille_octets / taille
			return f"{taille_lisible:.2f} {unite}"
	
	# Si la taille est inférieure à 1 octet
	return "0 o"



# Fonction de remplacement de placeholder
def placeholder_replace(text, placeholder_form, placeholder_dict):
	
	# Fonction de récupération 
	def replace_fct(dct):

		def replace_match(match):

			key = match.group(1)
			return dct.get(key, f'<{key} not found>')

		return replace_match

	return re.sub(
		placeholder_form, 
		replace_fct(placeholder_dict), 
		text
	)


