# -*-coding:Utf-8 -*

# Ressources tkinter étendues du framework
# Le contenu ne doit pas changer

# Modules requis
import tkinter as tk



# Classe d'ajout de méthodes pour tk.TK et tk.Toplevel
class WindowFunctions():

	# Fonction de centrage d'un élément
	def centerScreen(self):

		# Mise à jour de l'affichage
		self.update()
		
		# Positionnement au centre de l'écran
		dim_taskbar = 31
		dim_menubar = 30
		x_cordinate = int((self.winfo_screenwidth() - self.winfo_width() ) / 2)
		y_cordinate = int((self.winfo_screenheight() - self.winfo_height() - dim_taskbar - dim_menubar) / 2)
		self.geometry("+{}+{}".format(x_cordinate, y_cordinate))

		# Mise à jour de l'affichage
		self.update()



	# Fonction d'affichage de l'élément au dessus des autres
	def putOnTop(self, always=False):
		self.lift()
		self.attributes('-topmost',True)

		if always == False:
			self.after_idle(self.attributes,'-topmost',False)



# Extension de tk.Tk
class Tk(WindowFunctions, tk.Tk):
	pass



# Extension de tk.Toplevel
class Toplevel(WindowFunctions, tk.Toplevel):
	pass



# Extension de tk.Text qui peut être automatiquement redimentionnée
class Text(tk.Text):
	# Redéfinition de la méthode insert
	def insertResize(self, *args, **kwargs):
		# Insertion
		result = tk.Text.insert(self, *args, **kwargs)
		# Mise à jour de l'affichage
		self.update_idletasks()
		# Définition de la hauteur
		self.reset_height()

		return result

	# Méthode de mise à jour de la hauteur
	def reset_height(self):
		# Récupération de la hauteur en nombre de lignes
		height = self.tk.call((self._w, "count", "-update", "-displaylines", "1.0", "end"))
		# Définition de la hauteur
		self.configure(height=height)