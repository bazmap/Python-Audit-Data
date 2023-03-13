# Bazinga Py

## Introduction
Bazinga Py est un framework d'assistance à la conception d'application en Python avec une interface graphique.
Il ne repose que sur des modules standards évitant l'installation de composants spécifiques lors du déploiement de l'application sur d'autres systèmes.

Le principe est d'utiliser ce framework comme un module Python.
Celui-ci apporte alors les éléments suivants :
- Un sytème de gestion de fichiers de configuration
- Un système de gestion des arguments passés au programme
- Un système de gestion des logs
- Une base d'interface graphique
- Un ensemble de variables en lien avec l'application
- Un ensemble de fonctions utiles


## Utilisation
Le framework peut être placé n'importe où dans le répertoire du programme à développer.
Pour l'utiliser, il suffit de compléter le fichier `config.py` présent à la racine du framework puis d'utiliser le fichier `init.py` comme tout autre module Python.

L'image de l'écran d'accueil et l'icone peuvent être configurés à votre guise dans les variables `ba_app_var['log']['icon']` et `ba_app_var['log']['splash_screen']`.


## API
Le fichier init.py donne accès aux fonctionnalités suivantes :
- `ba_app_var`
- `ba_logger`
- `ba_functions`
- `ba_tk`
- `ba_rootWindows`

### ba_app_var
#### Variable
`ba_app_var` est une variable de type dictionnaire stockant presque tous les paramètres de l'application.

Parmis ces information on retrouve les clés suivantes :
- Timestamp de démarrage du programme  
  `ba_app_var['execution_date']`
  
- Informations sur le framework  
  `ba_app_var['framework']`
  - `ba_app_var['framework']['name']` : nom
  - `ba_app_var['framework']['version']` : version
  - `ba_app_var['framework']['dir']` : répertoire d'installation
  
- Informations sur le programme  
  `ba_app_var['software']`
  - `ba_app_var['software']['name']` : nom
  - `ba_app_var['software']['version']` : version
  - `ba_app_var['software']['resume']` : descritpion
  - `ba_app_var['software']['author']` : auteur
  - `ba_app_var['software']['copyright']` : mention légale
  - `ba_app_var['software']['dir']` : répertoire d'installation
  - `ba_app_var['software']['config_dir']` : répertoire de stockage des fichiers de configuration
  - `ba_app_var['software']['config_file_default']` : fichier de configuration à utiliser par défaut
  - `ba_app_var['software']['logo']` : emplacement du logo de l'application (fichier gif)
  - `ba_app_var['software']['icon']` : emplacement de l'icone de l'application (fichier gif)
  - `ba_app_var['software']['splash_screen']` : emplacement de l'image de l'écran de démarrage de l'application (fichier gif).  
  Attention, la taille de l'image défini la taille de l'écran de démarrage, une taille de 640x360 est en générale assez bien adaptée.
  
- Informations sur les logs  
  `ba_app_var['log']`
  - `ba_app_var['log']['dir']` : répertoire de stockage des logs
  - `ba_app_var['log']['name']` : nom des fichiers de log
  - `ba_app_var['log']['prefix_to_delete']` : préfixe des fichiers de log à supprimer lors de la rotation.   
    Ce prefixe doit être présent dans `ba_app_var['log']['name']`.
  - `ba_app_var['log']['type']` : gestion des fichiers de log :
    - `simple` : un fichier de log est créé par execution. 
    - `rotating` : plusieurs fichiers de log peuvent être créées par execution : un nouveau est automatiquement créé lorsque le premier atteind 2Mo.
  - `ba_app_var['log']['nb_to_keep']` : nombre de fichier de log à conserver.
  - `ba_app_var['log']['min_level']` : niveau minimum des message à logguer parmis :
    - `NOTSET`
    - `DEBUG`
    - `INFO`
    - `WARNING`
    - `ERROR`
    - `CRITICAL`
  - `ba_app_var['log']['stdout_levels']` : liste des niveaux de log à afficher sur la sortie standard parmis :
    - `NOTSET`
    - `DEBUG`
    - `INFO`
    - `WARNING`
    - `ERROR`
    - `CRITICAL`
  
- Variables diverses de l'application :  
  `ba_app_var['var']`  
  Le développeur utilisant le framework peut ajouter librement autant de variables que désiré sous cette clé.

- Paramètres de l'application (que l'utilisateur du programme pourra modifier si le développeur lui a permi):  
  `ba_app_var['param']`
  - Paramètres fournis par défaut par le framework :  
    `ba_app_var['param']['framework']`
  - Paramètres définis par le développeur :  
    `ba_app_var['param']['config_framework']`
  - Fusion des paramètres du framework et de ceux définis par le développeur :  
    `ba_app_var['param']['software']`
  - Paramètres fournis par le fichier de configuration lu (si fichier il y a) :  
    `ba_app_var['param']['config_file']`
  - Paramètres fournis par les arguments passés au programme (si argument(s) il y a) :  
    `ba_app_var['param']['arg']`
  - Paramètres disponibles pour l'exécution du programme :  
    `ba_app_var['param']['init']`  
    **C'est la variable de configuration à utiliser sans tkinter !**
  - Paramètres disponibles pour l'exécution du programme via l'interface :  
    `ba_app_var['param']['init_tk']`  
    **C'est la variable de configuration à utiliser avec tkinter !**

La dernière variable `ba_app_var['param']` mérite un peu d'attention. En effet, elle a pour but de définir un ensemble de paramètres modifiables par l'utilisateur via un fichier de configuration, des arguments passés au programme ou directement dans l'interface.  


#### Paramétrage

La variable `ba_app_var` est personnalisable par le développeur du programme. Il faut pour cela éditer le fichier `config.py` à la racine du framework afin d'écraser les valeurs fournies par défaut ou de les compléter avec de nouvelles clés.

Différents paramètres doivent éventuellement pouvoir être modifiés par l'utilisateur final (via un fichier de configuration, des arguments passés au programme ou des valeurs définies dans l'interface de l'application). Ces paramètres doivent être stockés dans la variable `ba_app_var['param']`.

Le framework apporte les paramètres suivants :
- `configFile` : `ba_app_var['param']['framework']['configFile']` - nom du fichier de configuration à utiliser  
  defaut : `ba_app_var['config_file']['default_file']`
- `printConfigFile` : `ba_app_var['param']['framework']['printConfigFile']` - affichage d'un fichier de configuration type (dans la console).
- `logFileNumber` : `ba_app_var['param']['framework']['logFileNumber']` - nombre de fichir de log à conserver  
  defaut : `ba_app_var['log']['nb_to_keep']`  

Le développeur peut ainsi configurer autant de variables que nécessaire dans le fichier `config.py` dans la variable `ba_app_var['param']['config_framework']`. La déclaration de ces variables doit cependant respecter le modèle suivant :
```
app_var['param']['config_framework'] = {
	'ma_variable': {
		'input_scope' : ['argument','config'],
		'type' : 'boolean',
		'value' : False,
		'value_user' : None,
		'expected': 'True/False',
		'group': '',
		'label': 'Mon label',
		'help' : "Cette variable permet de faire quelque chose de très interessant."
	}
} 
```

Avec :
- `ma_variable` : mot clé utilisé pour appeler la variable ainsi que dans les arguments et le fichier de configuration.
- `input_scope` : fonction pouvant configurer la variable :
  - '`argument`' : en argument.
  - '`config`' : dans le fichier de configuration.
- `type` : type de donnée de la variable parmi :
  - '`string`'
  - '`boolean`'
  - '`integer`'
  - '`float`'
- `value` : valeur de la variable.
- `value_user` : valeur présentée à l'utilisateur lors de la génération d'un fichier de configuration type.  
  Par exemple la valeur vide `''` au lieu de `None` (nul).  
  Cette propriété ne doit pas être déclarée si elle n'est pas utilisée.
- `expected` : valeurs attendue et présentées comme aide à l'utilisateur.
- `group` : groupe auquel appartien la variable (utilisé dans les fichiers de configuration).
- `label` : texte utilisé comme label dans les widgets de l'application.
- `help` : description de la variable présentées comme aide à l'utilisateur.

Les variables présents par défaut (`ba_app_var['param']['framework']`) et celles apportées par le développeur (`ba_app_var['param']['config_framework']`) sont fusionnées au sein de la variable `ba_app_var['param']['software']`.

#### Fichier de configuration

Le framework permet l'utilisation de fichiers de configuration pour définir les variables présentes dans `ba_app_var['param']['software']`.

Toute variable fournie dans un fichier de configuration (même non listée dans `app_var['param']['software']`) sera récupérée et associée à la variable `app_var['param']['config_file']`.

Le fichier de configuration n'apportant qu'une information group/clé/valeur, seules les sous-clés suivantes sont disponibles :
- `value` 
- `group`

#### Fichier de configuration

Le framework permet l'utilisation d'arguments passés au programme pour définir les variables présentes dans `ba_app_var['param']['software']`.

Tout argument fourni (et listé dans `app_var['param']['software']`) sera récupéré et associé à la variable `app_var['param']['arg']`.

Le fichier de configuration n'apportant qu'une information clé/valeur, seules les sous-clés suivantes sont disponibles :
- `value` 

#### Utilisation

Le programme développé doit utiliser au choix :
- La variable `ba_app_var['param']['init']` si aucune interface n'est utilisée.
- La variable `ba_app_var['param']['init_tk']` si une interface est utilisée.

La variable `ba_app_var['param']['init']` est construite par aggrégation des autres variables dans l'ordre suivant :
1. `ba_app_var['param']['framework']`
2. `ba_app_var['param']['config_framework']`
3. `ba_app_var['param']['config_file']`
4. `ba_app_var['param']['arg']`
La valeur d'un argument écrase donc la valeur du fichier de configuration qui écrase la valeur définie par le programmeur.

La variable `ba_app_var['param']['init_tk']` est construite par aggrégation de `ba_app_var['param']['init']` avec les valeurs présente dans les widgets de l'interface dans l'ordre suivant :
1. `ba_app_var['param']['init']`
2. Valeur du widget
La valeur d'un widget écrase donc la valeur de la variable `ba_app_var['param']['init']`.

Notez que `ba_app_var['param']['init_tk']` est initialisée à l'instantiation de `ba_rootWindows()`, sinon elle n'est pas disponible.  
Voir la partie dédiée à `ba_rootWindows()` pour plus de précisions.


### ba_logger
Il s'agit de l'interface de log qui est basée sur le module `logging` fourni en standard avec Python.  
`ba_logger` est un objet `logging.logger` avec toutes ses methodes et initialisé avec les propriétés renseignées dans la variable `ba_app_var['log']`.  

Notez que le nom du logger (`logging.getLogger(name)`) est initialisé avec la variable `ba_app_var['log']['name']` ce qui ne permet pas l'utilisation de plusieurs instance de logger en parallèle.  

Pour logguer un message il suffit d'utiliser l'une des méthodes fournie par l'objet `logging.logger` :
- `ba_logger.debug(msg)`
- `ba_logger.info(msg)`
- `ba_logger.warning(msg)`
- `ba_logger.error(msg)`
- `ba_logger.critical(msg)`
- `ba_logger.exception(msg)`
- `ba_logger.log(level, msg)`  

Notez que l'objet `ba_logger` ne donne pas accès au module `logging` et que ce dernier devra donc être appelé si vous avez besoin de ses éléments.



### ba_functions
ba_fonction fourni une série de fonctions qui peuvent êtres utiles :
- `coalesce(*args)` : le premier argument non nul est renvoyé.
- `dprint(my_dict)` : affichage d'un dictionnaire.
- `checkFontAvailability(*fontName)` : la première police passée en argument et présente dans la liste des polices disponible est retournée.  
Si aucune des polices listées n'est disponible, alors la police par défaut est retournée.
- `set_mousewheel(widget)` : lie le défilement vertical d'un widget tkinter fourni au défilement de la molette.



### ba_rootWindows
`ba_rootWindows()` est une classe héritée de `ba_tk.Tk()` et permet l'initialisation de l'interface graphique de l'application.

L'appel à cette fenêtre se fait sous la forme suivante :  
`root = ba_rootWindows()`  
Il suffit ensuite d'utiliser `root` comme élément de base de l'interface du programme (le mot clé `root` est libre, tout autre nom peut être utilisé)

En plus des méthodes définies pour `ba_tk.Tk()` les méthodes suivantes sont disponibles :
- `openSplashScreen()` : ouvre l'écran d'accueil, l'objet `Toplevel()` associé est instancié dans `ba_rootWindows.splashScreen`.
- `openInfoScreen()` : ouvre l'écran d'information, l'objet `Toplevel()` associé est instancié dans `ba_rootWindows.infoScreen`.
- `openHelpScreen()` : ouvre l'écran d'aide, l'objet `Toplevel()` associé est instancié dans `ba_rootWindows.helpScreen`.
- `run_mainloop()` : ferme l'écran d'accueil et lance la méthode `tk.mainloop()`.

Notez que l'instanciation de `ba_rootWindows()` appelle la fonction `openSplashScreen()`. L'objet `Toplevel()` associé est détruit lors de l'appel à la méthode `run_mainloop()` : une fois le programme chargé. Il est possible d'empêcher le chargement de l'écran d'accueil avec l'argument `openSplashScreen = False` passé à la classe :
`root = ba_rootWindows(openSplashScreen = False)`

A l'instantiation de `ba_rootWindows()`, des variables de contrôle tkinter sont initialisées sur la base des variables de configuration (`ba_app_var['param']['init']['clé']`).  
Vous retrouverez ainsi la variable `ba_app_var['param']['init_tk']` qui possède la même structure que la variable de configuration `ba_app_var['param']['init']` avec une différence : la clé `'value'` de chaque variable est une variable de contrôle tkinter instanciée au lieu d'une simple valeur. Il faudra donc utiliser les méthodes `.set()` et `.get()` pour définir et récupérer la valeur.  
Voici la structure de `ba_app_var['param']['init_tk']` pour une clé :
```
app_var['param']['config_framework'] = {
	'ma_variable': {
		'input_scope' : ['argument','config'],
		'type' : 'boolean',
		'value' : False,
		'value_user' : None,
		'expected': 'True/False',
		'group': '',
		'label': 'Mon label',
		'help' : "Cette variable permet de faire quelque chose de très interessant."
	}
} 
```


La fenêtre principale `ba_rootWindows()` possède un menu référencé sous le nom `ba_rootWindows.rootMenuBar`.
Deux sous-menus sont présents :
- `ba_rootWindows.rootMenuBar.menu_fichier`
- `ba_rootWindows.rootMenuBar.menu_aide`



### ba_tk
`ba_tk` est un module qui étant les possibilités de tkinter en redéfinissant certains objets :
- `Tk()` et `Toplevel()` - ajout des méthodes suivantes :
  - `centerScreen(element)` : centrage automatique d'une fenêtre tkinter
  - `putOnTop(element, always=False)` : affichage d'une fenêtre trkinter (`tk.Tk()` ou `tk.Toplevel()`) au premier plan.  
L'argument `always` permer de spécifier si la fenêtre doit recouvrir les autres programmes et maintenir ce recouvrement.
- `Text()` - ajout de la méthode suivante :
  - `insertResize()` : redimentionne automatiquement le widget à chaque insertion d'une nouvelle ligne.
