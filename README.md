# ORPhÉE

ORPhÉE (Outil de Reprise de Photographies et Éléments Embarqués) est une application produite au Département de l’administration des données (DAD) des Archives nationales, dans le cadre de la reprise des données des reportages photographiques de la Présidence de la République. Elle a pour fonction la fabrication de paquets d’archives (SIP) en vue de leur versement dans le SAE Vitam des Archives nationales. Son intérêt principal par rapport aux autres outils de fabrication de SIP est sa capacité à extraire les métadonnées internes des photographies, y compris les métadonnées descriptives qui ont pu être renseignées par le photographe (description, mots-clés, nom du photographe, lieux de la prise de vue).
Une version paramétrable de l’outil a été produite, permettant son utilisation dans des contextes différents :
1) Renseignement à l’aide d’un formulaire de certaines valeurs qui étaient inscrites « en dur » dans l’application originale (ex : identifiant du service d’archive, du service producteur et du service versant, type de contrat des photographes) ;
2) Choix des champs de métadonnées internes à extraire.
Ce guide a pour but d’accompagner les archivistes extérieurs au DAD dans l’utilisation de l’application, mais aussi d’en présenter le fonctionnement et les modalités d’utilisation. En effet, son usage s’inscrit spécifiquement dans le contexte Vitam et peut ne pas convenir à d’autres solutions d’archivage électronique. Elle nécessite par ailleurs un nettoyage des données et la production d’un fichier de métadonnées externes selon des critères très spécifiques.

Le dossier "orphee_ui" contient le code de l'application avec interface utilisateur.
Le dossier "orphee_dad" contient le code original de l'application adapté au contexte spécifique de la reprise des reportages photographiques des Présidents de la République aux Archives nationales.
Le dossier "executables" contient les fichiers exe des deux versions du code.

## 1. Traitements des données et prérequis

### 1.1. Prérequis logiciels

Pour le calcul des métadonnées de format, ORPhÉE nécessite l'installation préalable de l'application Siegfried (https://www.itforarchivists.com/) sur les postes utilisés pour la fabrication de paquets.

### 1.2. Prérequis de classement
L’application a été conçue pour traiter des reportages se présentant sous la forme d’une arborescence de dossiers et de sous-dossiers. Elle permet de reconstituer cette arborescence afin de conserver la structure originelle du fonds.
Chaque reportage doit disposer d’un identifiant unique à l’échelle du versement (il peut s’agir d’un numéro, ex : 001) et se présenter sous la forme d’un dossier dont le nom contient cet identifiant. L’identifiant sera repéré par l’application s’il se présente sous une des formes suivantes : 
* Suivi d’une espace (ex : « 001 Investiture du président »)
* Suivi d’un tiret bas (ex : « 001_Investiture du président »)
* À la fin du nom du dossier (ex : « Reportage 001 »)
Assurez-vous que l’identifiant correspond à une chaine de caractères ne contenant ni caractères spéciaux ni espace : dans le cas des reportages « bis » par exemple, l’identifiant peut être « 001Bis », mais ne peut pas être « 001 Bis ». La casse n’est en revanche pas prise en compte : « 001b » et « 001B » seront considérés comme un même identifiant.

### 1.3. Nettoyage des données
Une partie du nettoyage des données est effectué par l’application qui exclut automatiquement certains fichiers système et fichiers masqués sur des critères de nommage.
Les fichiers contenant dans leur nom les chaînes suivantes ne sont pas traités et sont donc exclus du paquet : 
*	DS_Store
*	Thumbs
*	BridgeSort
*	PM_lock
*	desktop.ini
*	._


Des analyses et nettoyages préalables sont cependant nécessaires en amont de l’utilisation de l’application. La présence de chemins trop longs et de certains caractères spéciaux dans les nommages de dossiers et de fichiers peuvent empêcher le bon fonctionnement de l’application. 
*	Les chemins des fichiers ne doivent pas dépasser 255 caractères.
*	Les caractères spéciaux et accentués doivent être supprimées ou remplacés dans les noms de dossiers et de fichiers, par exemple à l’aide du logiciel AntRenamer. Exemple de caractères problématiques :
    -	Les lettres accentuées ;
    -	Les tirets longs et moyens (— ; –) ;
    -	Les espaces insécables ;
    -	La chaîne « espace + tiret + espace » ;
    -	Deux espaces consécutives ;
    -	L’apostrophe typographique ;
    -	Les icônes (ex : ☎, ✂).

### 1.4.	Préparation des fichiers de données


#### 1.4.1.	Le CSV de métadonnées externes
Le csv de métadonnées ingéré par la moulinette doit reprendre les informations présentes dans l’instrument de recherche. 
Le csv ingéré par le scriptCe csv doit impérativement prendre la forme suivante : 
Identifiant du Numéro de reportage ; Titre du reportage ; Date de début ; Date de fin
La colonne contenant le numérol’identifiant de reportage doit être au format Texte afin d’éviter la perte des « 0 » en début de chaîne (ils qui seront supprimés si les cellules sont au format Nombre). Assurez-vous également qu’il n’y a pas d’espaces en début ou fin de chaîne.
Les dates doivent être au format suivant : JJ.MM.AAAA
Une cinquième colonne contenant la coôte des unités d’archive de niveau reportage peut être ajoutée et entraînera la création des balises SEDA correspondantes. Attention à ne pas ajouter une cinquième colonne contenant une autre information : ses valeurs seront automatiquement interprétées comme étant les coôtes des articles et seront ajoutées au manifest en tant que telles. 


#### 1.4.2.	La liste de reportages
Confrontés aux restrictions de volumétrie imposées par le SAE des Archives nationales, qui n’accepte pas de SIP de plus de 30Go en entrée unitaire à l’heure actuelle, nous avons envisagé plusieurs méthodes de sélection des reportages à intégrer à chaque SIP. 
La copie de l’ensemble des reportages sélectionnés dans un répertoire spécifique qui serait intégré au SIP dans son ensemble posait plusieurs problèmes : 
* Le risque de perte de données au cours de la copie des fichiers dans ce répertoire « tampon » ;
* Le risque de copier plusieurs fois certains reportages, ou au contraire d’en oublier dans le contexte d’une copie en masse (par exemple si ceux-ci n’apparaissent pas dans l’ordre alphabétique dans le répertoire d’origine) ;  
* Le délai nécessaire à la copie des fichiers vers l’espace tampon.
Une solution basée sur des limites volumétrique imposées à l’application a également été écartée, dans la mesure où elle ne permettait pas au fabricateur du SIP de contrôler le contenu du paquet : 
* Risque d’import de reportages non consécutifs ;
* Empêche une sélection selon une logique intellectuelle qui pourrait être souhaitée par le fabricateur (regroupement selon des critères temporels ou de communicabilité par exemple).
La solution retenue est celle d’un fichier texte importé dans l’application et dans lequel se trouvent l’ensemble des identifiants des reportages à ajouter au paquet. Chaque identifiant de reportage doit occuper une ligne, sans ajout de séparateur ni d’espace. Ils doivent apparaître dans l’ordre dans lequel on souhaite que les reportages apparaissent dans le SIP. Si les identifiants sont correctement triés dans le csv de métadonnées externes, alors il suffit de copier les cellules de la colonne correspondant aux identifiants des reportages à ajouter et de les coller dans le fichier texte.
Nota : Cette étape peut être fastidieuse, notamment pour les reportages « bis » qui risquent de ne pas apparaître au bon endroit lorsque le csv est trié en suivant l’ordre des numéros identifiants de reportage.


#### 1.4.3.	Points de vigilance
1) Veiller à ce que les numéros identifiants de reportage du fichier csv et du fichier texte soient identiques à ceux présents dans les noms des dossiers de reportages. Apporter une attention particulière aux reportages avec des identifiants spéciaux, par exemple avec la mention « bis », qui peut être écrite en toutes lettres ou seulement indiquée par la lettre « B ». Le cas échéant, il n’est pas nécessaire de corriger les différences de casse : pour la reconnaissance des numéros identifiants de reportages, la moulinette passe automatiquement la chaîne en minuscules. 
2) Veiller à ce que les fichiers csv et txt soient bien encodés en UTF-8.
3) Dans la colonne « Numéro/identifiant du reportage » comme dans le fichier texte, veiller à ce que chaque ligne non vide contienne bien un numéro identifiant de reportage valide. Toute chaîne de caractères identifiée dans la colonne « Numéro/identifiant du reportage » ou dans une ligne du fichier texte peut servir de valeur pivot et donc remonter des informations erronées : par exemple, une cellule ne contenant qu’une espace sera associée à l’ensemble des dossiers dont le nom contient contenant au moins une espace dans leur nom.


## 2.	Mode d’emploi détaillé de l’application


### 2.1.	Le formulaire
Pour s’adapter à des contextes différents de celui dans lequel l’application a été originellement créée, mais aussi pour faciliter son l’utilisation de l’application, un formulaire a été créé. Il peut être divisé en quatre parties : 
* Les informations à renseigner ;
* Le choix des métadonnées internes à extraire ;
* Le rattachement à une autre unité d’archive (optionnel) ;
* L’import des données et des fichiers de métadonnées externes (liste des reportages et instrument de recherche).

  
#### 2.1.1.	Les informations à renseigner
Les deux premières informations à fournir sont le numéro d’entrée du paquet et le numéro du paquet. Ces informations seront ensuite fusionnées et complétées afin de créer le contenu de l’élément SEDA ArchivalAgencyArchiveUnitIdentifier de chaque unité d’archive, c’est-à-dire la nouvelle cote de l’UA dans le SAE numérique.

* Intitulé du versement : contenu des éléments SEDA Comment et MessageIdentifier.
* ArchivalAgency Identifier : nom du service d’archives auquel sera versé le paquet (ex : Archives nationales).
* TransferringAgency : nom du service versant (ex : Service photographique de la Présidence).
* OriginatingAgency Identifier : identifiant du service producteur (ex : FRAN_NP_009886).
* SubmissionAgency : identifiant du service versant (ex : FRAN_NP_009886).
* ArchivalAgreement : référence à un contrat d’entrée (ex : FRAN_CE_0001).
* AuthorizedAgent Activity : activité de la personne détenant des droits sur le fichier et dont le nom sera extrait des métadonnées internes. Il s’agit probablement du photographe, mais la valeur du champ peut être adaptée aux différents contextes de production. Notez que cet élément ne sera créé que si le service producteur a renseigné au préalable un des champs de métadonnées suivants : a été renseigné au préalable par le service producteur ( By-line, Artist, Creator).
* AuthorizedAgent Mandate : type de contrat liant le détenteur de droits aux photographies. S’agit-il d’un photographe agent de service public, d’un photographe privé, d’un photographe d’agence de presse ? Notez que cet élément ne sera créé que si le service producteur a renseigné au préalable un des champs de métadonnées suivants a été renseigné au préalable par le service producteur : By-line, Artist, Creator.


Pour les deux éléments enfants de AuthorizedAgent évoquésez ci-dessus, notez que les valeurs choisies seront associées automatiquement à l’ensemble des fichiers pour lesquelles la métadonnée a été extraite. Si les situations varient entre les détenteurs de droits associés aux fichiers traités, il sera nécessaire de modifier le code de l’application ou de modifier manuellement le manifest après sa création par l’application. 
* ArchivalProfile : référence au profile d’archivage applicable aux unités d’archive (ex : FRAN_PR_0001).
* AcquisitionInformation : modalité d’entrée des archives (ex : versement, don).


#### 2.1.2.	Le choix des métadonnées à extraire
À l’aide des fonctions du logiciel Exiftool , les métadonnées descriptives internes renseignées par les photographes ou iconographes du service producteur peuvent être extraites et ajoutées aux balises SEDA correspondantes dans les ArchiveUnit de niveau « photographie ». Dans cette partie du formulaire, chaque case cochée correspond à un champ de métadonnées que l’utilisateur souhaite extraire des fichiers pour l’ajouter au manifest. 


| **Métadonnée**                               | **Description**                                       | **Balise(s) SEDA**                         |
|---                                           |---                                                    |---                                         |
| -CreateDate                                  | Date de création du fichier dans l’appareil photo	    | Content/StartDate et EndDate               |
| -FileModifyDate	                             | Date de dernière modification du fichier.	            | BinaryDataObject/FileInfo/LastModified     |
| -By-line, -Artist, -Creator	                 | Nom du photographe.	                                  | Content/AuthorizedAgent/FullName           |
| -Country, -Country-PrimaryLocationName       |	Lieu de la prise de vue (pays).	                      | Coverage/Spatial                           |
| -City                                        |	Lieu de la prise de vue (ville).                      | Coverage/Spatial                           |
| -Caption-Abstract, -Description	             | Légende de la photographie.	                          | Content/Description                        |
| -Subject, -Keywords                          | Mots-clés.                                            | Content/Tag                                |


Comme l’indique le tableau ci-dessus, plusieurs éléments peuvent correspondre à deux voire trois champs de métadonnées internes. Si un travail d’analyse des métadonnées a été réalisé en amont, il conviendra de choisir le champ le mieux renseigné au sein du fonds traité. Si plusieurs champs correspondant à une même balise SEDA sont cochés, celles-ciles métadonnées seront traitées selon un ordre de priorité : 
* AuthorizedAgent/FullName : la valeur choisie en priorité sera celle du champ « By-line », si celui-ci est vide celle du champ « Artist », et si cellece dernier-ci est vide aussi celle du champ « Creator ».
* Coverage/Spatial : la valeur choisie en priorité sera celle du champ « Country », et si celui-ci est vide celle du champ « Country-PrimaryLocationName ».
* Content/Description : la valeur choisie en priorité sera celle du champ « Caption-Abstract », si celui-ci est vide celle du champ « Description ».
* Content/Tag : la valeur choisie en priorité sera celle du champ « Subject », si celui-ci est vide celle du champ « Keywords ».
Il est important de noter néanmoins que la présence et la pertinence des métadonnées internes sont tributaires de la qualité du travail d’indexation réalisé par le service producteur : si ces métadonnées n’ont pas été renseignées, ou si elles ont été mal renseignées, cela se reflètera dans le manifest produit.


#### 2.1.3.	Le rattachement à une autre unité d’archive
L’application offre la possibilité de créer un paquet qui pourra ensuite être rattaché à une unité d’archive déjà versée dans le SAE. S’il souhaite effectuer un rattachement, l’utilisateur doit cocher la case et renseigner deux informations : 
* la valeur de la balise <ArchivalAgencyArchiveUnitIdentifier> de l'UA de rattachement
* la valeur de la balise <Title> de l'UA de rattachement.
Cette option entraîne la création d’une unité d’archive « fantôme », correspondant à l’unité d’archive déjà versée à laquelle les reportages du paquet seront ensuite rattachés. Ainsi, au lieu d’apparaître en râteau dans le manifest, l’ensemble des reportages du paquet seront des éléments enfants de cette UA fantôme. Cette dernière n’apparaîtra pas dans le SIA numérique après le rattachement du SIP l’unité d’archive choisie.
L’ArchiveUnit de l’UA fantôme aura un élément <Management> avec la structure suivante : 
 

#### 2.1.4.	L’import des données et des fichiers de métadonnées externes
L’utilisateur doit ensuite sélectionner les répertoires et fichiers sur lesquels l’application va se baser pour la constitution du paquet : le répertoire parent contenant l’ensemble des dossiers de reportages à traiter ; le répertoire cible où seront créés le manifest et le dossier content ; le fichier csv avec les métadonnées issues de l’instrument de recherche ; la liste des reportages au format texte. 


### 2.2.	Suivi des opérations en cours
Après avoir soumis le formulaire, l’application va commencer la fabrication du SIP. L’utilisateur est informé de la progression des traitements effectués par des messages signalant les opérations en cours : 
* Extraction des métadonnées internes des photos.
* Création de l'en-tête du manifest.
* Création des DataObjectGroup.
* Ajout des métadonnées aux DataObjectGroup.
* Création des éléments ArchiveUnit.
* Suppression des doublons dans les DataObjectGroup.
* Attribution des identifiants.
* Création de l'élément DescriptiveMetadata.
* Écriture du manifest.
* Copie et renommage des fichiers dans le dossier content.

Certaines étapes peuvent être longues, notamment l’extraction des métadonnées internes. À titre indicatif, la constitution d’un paquet de 20Go peut prendre entre 10min et 20min, celle d’un paquet de 60Go entre 20min et 30min, et celle d’un paquet de 100Go entre 40min et 1h. 
La fermeture de l’application arrêtera le processus de création du SIP : celle-ci elle ne doit donc être fermée qu’en cas d’erreur ou de dépassement des délais évoqués ci-dessus. 
La fermeture de l’application arrêtera le processus de création du SIP, veillez donc à ne pas interrompre le processus simplement car, même si rien ne semble se passer. Il arrive qu’ORPhÉE soit « bloqué ». Si une étape semble durer plus longtemps qu’elle ne le devrait, appuyez une fois sur « Entrée ». Si les étapes suivantes se déclenchent immédiatement, il s’agissait d’un simple blocage. S’il ne se passe rien, c’est qu’il est encore en train de travailler : laissez-lui un peu plus de temps. Si les délais évoqués ci-dessus sont largement dépassés, ou si un message d’erreur apparait, vous pouvez fermer l’application.


### 2.3.	Gérer les erreurs les plus fréquentes
#### 2.3.1.	Problème d’identification de la donnée pivot : l’identifiant e numéro de reportage
Si un numéro identifiant de reportage présent dans le fichier texte n’est pas trouvé parmi les dossiers, le message « ERREUR : Le reportage X n'a pas été trouvé dans le répertoire Y. » s’affichera pendant l’étape d’extraction des métadonnées internes des photos et la moulinette sera interrompue.
Que faire ? 
*	Vérifier l’identifiant e numéro de reportage : la forme présente dans le nom du dossier est peut-être légèrement différente de celle inscrite dans les fichiers csv et texte.
*	Vérifier que vous disposez bien de ce reportage : le dossier correspondant est-il présent dans les fichiers ? Si non, il est peut-être mal rangé : il est possible qu’il ait été malencontreusement glissé dans un autre dossier de reportage. Une recherche sur l’identifiant e numéro de reportage dans l’explorateur Windows devrait permettre de le débusquer !
*	Vérifier que le reportage existe bien en vous référant à l’instrument de recherche : s’il s’agit de numéros, il peut y avoir un « trou » dans la numérotation des reportages.


#### 2.3.2.	Les fichiers système et fichiers cachés
Certains fichiers systèmes (qui ne sont pas à conserver), tels que les « desktop.ini », ne sont pas identifiés par tous les composants de la moulinette et entraînent donc des incohérences au sein des données à traiter. Ces incohérences peuvent ensuite provoquer une erreur qui va interrompre la moulinette. L’erreur peut prendre la forme suivante : « AttributeError : ‘NoneType’ object has no attribute ‘split’ ».
Comment identifier le(s) fichier(s) à supprimer ?
* Chercher le(s) fichier(s) problématique(s) à l’aide d’un export DROID
* Utiliser la version « debug » de la moulinette qui devrait afficher le nom du fichier problématique au moment où il cause une erreur. Cette solution ne permettra d’identifier que le premier fichier à causer une erreur et ne permet donc pas d’identifier plusieurs fichiers problématiques (l’opération sera alors à répéter jusqu’à ce que tous cles fichiers aient été supprimés).


#### 2.3.3.	Les chemins de fichier trop longs ou caractères spéciaux
La présence de chemins trop longs et de certains caractères spéciaux dans les nommages de dossiers et de fichiers empêche le bon fonctionnement de l’application et provoque une erreur de balise vide. Celle-ci est due au fait queEn effet, les logiciels appelés par la moulinette (Siegfried et Exiftool), ne reconnaissent pas les chemins trop longs ou contenant un caractère spécial et les excluent de leur traitement. Cette situation peut entraîner deux types d’erreurs :
1)	Une erreur lors de l’extraction des métadonnées : le chemin contenant un caractère spécial est mal interprété par l’application qui ne le retrouve pas dans l’arborescence. Au lieu de récupérer les métadonnées extraites, l’application ne récupère donc rien. Apparait alors une erreur ExiftoolOutputEmptyError indiquant que « execute_json expected output on stdout but got none ».
2)	Une erreur lors de l’écriture du manifest : certains éléments associés aux fichiers dont le chemin a posé un problème ne sont pas créés, p. Par exemple l’élément <BaliseTemp> qui contient l’empreinte calculée par Siegfried. Lorsque le contenu de la BaliseTemp est ensuite récupéré, celle-ci n’ayant jamais été créée, la moulinette affiche une erreur indiquant qu’un élément None n’a pas d’attribut « text » : « NoneType has no attribute ‘text’ »


## 3.	Fonctionnement du script


### 3.1.	Traitement des données importées
Les informations renseignées dans le formulaire se présentent dans l’application sous la forme d’un dictionnaire Python, composé de clés et de valeurs. Les métadonnées renseignées dans la première partie seront appelées à différents endroits du script pour les inscrire à leur place dans le manifest. Les autres informations sont traitées dans la première partie du processus.
*	select_csv() récupère dans le formulaire le chemin vers le fichier csv créé à partir de l’instrument de recherche, encodé en UTF-8, et contenant les informations suivantes : numéro identifiant due reportage, titre du reportage, date de début, date de fin. La fonction retourne le contenu du fichier sous la forme d’une liste de listes (une liste par ligne du csv, donc une liste par reportage).
*	select_list_rp() récupère dans le formulaire le chemin du fichier texte contenant la liste des numéros identifiants des reportages à ajouter au SIP. La fonction transforme le contenu du fichier en une liste Python.
*	 chose_target_dir() récupère dans le formulaire le chemin vers le répertoire dans lequel seront créés le manifest XML et le dossier « content » où seront copiés à plat les fichiers renommés. La fonction transforme le chemin et crée un dossier « content » vide.


### 3.2.	L’extraction et la fusion des métadonnées internes
Les trois fonctions suivantes ont pour objectif l’extraction des métadonnées internes des fichiers à l’aide d’un logiciel de calcul d’empreinte et d’identification de format, Siegfried, et de la librairie PyExiftool qui permet une extraction des métadonnées internes des photos selon les mêmes modalités que le logiciel Exiftool. 


#### 3.2.1.	PyExiftool
La fonction exif_extract() prend comme arguments le chemin du répertoire (dir_path) contenant les reportages et la liste des reportages à ajouter au SIP. La fonction parcourt chaque numéro identifiant de reportage dans la liste et chaque élément (item) présent dans le répertoire (dir_path). Si un numéro identifiant présent dans la liste n’est pas identifié trouvé dans les noms de dossier, la moulinette est interrompue et renvoie un message d’erreur indiquant l’identifiant e numéro du reportage qui n’a pas été identifiétrouvé. Si tous les numéros identifiants sont identifiéstrouvés, elle boucle sur l’ensemble des dossiers correspondants (item) et recrée leur chemin (item_path) en concaténant le chemin du répertoire (dir_path) au nom de l’élément (item). Dans la même boucle, à l’aide de la fonction execute_json() de la librairie PyExiftool, les métadonnées internes de l’ensemble des fichiers contenus dans le dossier sélectionné sont extraites au format json. 
La syntaxe est similaire à celle du logiciel en ligne de commande Exiftool :
-r permet de traiter de manière récursive les fichiers dans les sous-répertoires.
-b permet d’extraire les métadonnées demandées au format binaire. Ce paramètre est utilisé pour contourner certains problèmes causés par les différences d’encodage au sein des métadonnées internes.
Vient ensuite la liste des métadonnées internes extraites. Les métadonnées renseignées en dur dans le script sont essentielles à son fonctionnement : FileName correspond au nom du fichier et Filesize à sa taille. L’ajout d’un « # » permet d’obtenir la valeur de cette métadonnée en octets telle qu’elle est attendue par le SAE, et non sous une forme plus facilement lisible par un humain, en kilo-octet ou mégaoctet par exemple. Les autres métadonnées internes sont importées à partir du formulaire (les valeurs associées à la clé « Champs_metadata ») et correspondent aux cases cochées par l’utilisateur. 
La variable « item_path » fournit le chemin du dossier du reportage traité dans cette boucle. 
Les métadonnées extraites sont ensuite ajoutées à une liste retournée à la fin de la fonction, et contenant donc ainsi l’ensemble des métadonnées extraites par Exiftool pour les reportages sélectionnés. Il s’agit donc d’une liste contenant autant de dictionnaires qu’il y a de reportages à ajouter au paquet. Chaque dictionnaire est constitué d’un ensemble de clés et de valeurs : chaque clé correspond au nom de la métadonnée extraite (CreateDate, By-line, City, etc) et la valeur associée correspond à la métadonnée en elle-même (la date de création du fichier, le nom du photographe, le nom de la ville où a eu lieu la prise de vue).


#### 3.2.2.	Siegfried
Le logiciel Siegfried est appelé à l’aide du module subprocess qui permet d’exécuter des programmes externes à partir du code Python, à condition bien sûr que le programme soit bien installé sur l’ordinateur. Ainsi, la fonction siegfried() appelle le logiciel Siegfried et agit de façon similaire à la fonction exif_extract() : elle prend comme arguments le chemin du répertoire (dir_path) contenant les reportages et la liste des reportages à ajouter au SIP. Elle parcourt ensuite chaque numéro de reportage dans la liste et chaque élément (item) présent dans le répertoire (dir_path). Elle boucle sur l’ensemble des dossiers correspondants (item) et recrée leur chemin (item_path) en associant le chemin du répertoire (dir_path) au nom de l’élément (item). Le logiciel Siegfried est ensuite exécuté à l’aide du module subprocess.run selon la même logique que lorsqu’il est utilisé en ligne de commande.  
 
-sf sert à signaler qu’on exécute le logiciel Siegfried.
-hash indique qu’on souhaite calculer l’empreinte des fichiers traités, et la valeur suivante (ici « sha512 ») indique l’algorithme de hachage qu’on souhaite utiliser (ici, celui demandé par la solution Vitam).
Les arguments suivants indiquent qu’on souhaite récupérer la sortie produite par le logiciel Siegfried sous la forme d’une chaine de caractères encodée en UTF-8.
Nous savons que les données produites par Siegfried sont au format json : nous utilisons donc le module json.loads() pour qu’elles soient interprétées correctement par le script. Les métadonnées du reportage sont ensuite ajoutées à une liste retournée à la fin de la fonction, et contenant donc l’ensemble des métadonnées calculées par Siegfried pour les reportages sélectionnés.


#### 3.2.3.	Fusion des métadonnées internes
Pour simplifier leur appel au cours des différentes étapes du pipeline de données, la fonction metadata_json() fusionne les métadonnées calculées par Siegfried avec celles extraites par Exiftool. La fonction parcourt d’abord chaque reportage dans les métadonnées issues de Siegfried et identifie l’ensemble des fichiers de ce reportage. Elle parcourt ensuite ces fichiers, et, pour chacun, identifie le chemin de ce fichier. La fonction cherche ensuite le même chemin dans les métadonnées extraites par Exiftool. Lorsqu’une correspondance est trouvée, la fonction fusionne les métadonnées Exiftool et Siegfried pour que l’ensemble des métadonnées d’un fichier soient stockées au même endroit. 


### 3.3.	Création du manifest
La fonction creer_root() permet de créer l’élément racine du manifest XML (ArchiveTransfer) et les éléments de l’en-tête dont les valeurs demeurent fixes tant que le script est utilisé pour la reprise des reportages photographiques de la Présidence de la République aux Archives nationales. 


### 3.4.	Création des DataObjectGroup
La fonction create_dataobjectgroup() parcourt de manière récursive l’ensemble des fichiers dans les dossiers du répertoire spécifié, reconstitue leur chemin, puis vérifie que ce chemin contient bien l’identifiant e numéro d’un reportage sélectionné. Elle établit par ailleurs une correspondance avec les données issues de l’instrument de recherche au format csv et vérifie que l’identifiante numéro de reportage demandé est bien présent dans l’instrument de recherche.
Elle repère ensuite les fichiers système et cachés à partir de leur nommage  afin de les exclure de la reprise. Elle crée ensuite, puis crée un élément DataObjectGroup pour chaque fichier dont il a été déterminé qu’il devait être repris. Ces DataObjectGroup sont des éléments enfant de l’élément DataObjectPackage créé par la fonction creer_root(). Ils ont eux-mêmes plusieurs éléments enfant créés par create_dataobjectgroup() mais dont la valeur n’est pas encore renseignée. Seule la valeur de l’élément Filename est renseignée : elle correspondra à terme au nom du fichier, mais à ce moment de la création du manifest, la valeur utilisée est le chemin du fichier. En effet, de nombreux fichiers ayant le même nom, le chemin constitue une valeur pivot plus fiable qui permettra par la suite de retrouver les métadonnées internes du fichier.
C’est justement la fonction package_metadata() qui itère sur l’ensemble des éléments DataObjectGroup et parcourt les métadonnées Exiftool et Siegfried pour identifier les correspondances entre les valeurs des éléments Filename et les chemins de fichiers tels qu’ils ont été enregistrés lors des extractions par Exiftool et Siegfried. Pour chaque fichier, elle associe ensuite chaque élément du DataObjectGroup à sa métadonnée interne correspondante : taille, date de dernière modification, empreinte, nom, type mime et identifiant du format. Enfin, dans l’élément Filename, le chemin du fichier est remplacé par son nom. 


### 3.5.	Création des ArchiveUnit : Niveau Reportage
La fonction up_rp() crée dans un premier temps un élément DescriptiveMetadata comme enfant de DataObjectPackage. DescriptiveMetadata contiendra les éléments ArchiveUnit dont l’imbrication permettra de reconstituer l’arborescence des dossiers. Chaque ArchiveUnit disposera d’un élément Content dont les éléments enfant correspondront aux métadonnées descriptives de cette unité d’archive. 
À l’instar de la fonction create_dataobjectgroup(), ua_rp() commence par rechercher des correspondances entre les dossiers présents dans le répertoire fourni et les numéros identifiants de reportages figurant dans la liste et dans l’instrument de recherche. Pour chaque dossier correspondant à un reportage sélectionné et présent dans l’instrument de recherche, un élément ArchiveUnit est créé. Il contient un élément Content dans lequel sont créées les métadonnées: 
DescriptionLevel : RecordGrp (puisqu’il s’agit d’un dossier).
Title : le titre du reportage issu de l’instrument de recherche.
ArchivalAgencyArchiveUnitIdentifier : l’élément, vide pour le moment, où sera renseignée la nouvelle cote de l’unité d’archive.
OriginatingAgencyArchiveUnitIdentifier : l’identifiant attribué à l’unité d’archive par le service producteur, c’est-à-dire l’identifiant e numéro du reportage (issu de l’instrument de recherche). Pour les versements des mandatures Hollande et Sarkozy, il n’existe pas de description au reportage. Les reportages n’étant pas cotés, leur identifiant est inséré dans cette balise. Il conviendra de la modifier pour les reportages de la mandature Chirac qui, eux, disposent bien d’une cote.
Description : contient simplement l’identifiant du e numéro de reportage (précédé de la mention « Reportage n° »). Cet élément a été ajouté dans un souci d’accessibilité : la balise OriginatingAgencyArchiveUnitIdentifier n’étant pas interrogeable dans le SAE des Archives nationales, l’ajout de la balise Description, interrogeable, permet de retrouver un reportage par son numéroidentifiant.
OriginatingAgency/Identifier et SubmissionAgency/Identifier  : l’identifiant du service producteur et du service versant. Leurs valeurs sont inscrites « en dur » dans le script.
StartDate / EndDate : les dates de début et de fin du reportage (il s’agit généralement de la même date).
Une fois l’ArchiveUnit/Content de niveau reportage créée, il s’agit de créer les ArchiveUnit de niveau inférieur (sous-dossiers, fichiers) à l’intérieur de cette première ArchiveUnit, afin de reproduire l’arborescence du reportage. Nous appelons donc la fonction sub_unit() à l’intérieur de la fonction up_rp(), qui prend en entrée le chemin du reportage, les métadonnées internes, les métadonnées de l’instrument de recherche et la liste des reportages. 
En cas de rattachement
Si l’utilisateur a choisi d’effectuer un rattachement, alors la valeur de la variable « rattachement » est non nulle, ce qui fait prendre à la fonction up_rp() une direction légèrement différente : un niveau « fantôme » qui regroupera l’ensemble des reportages du paquet est créé à partir des informations fournies par l’utilisateur (ex : un niveau « 2016 »). À cette UA fantôme sont assignées des règles de gestion spécifiques avec un élément Management : 
Management/UpdateOperation/ArchiveUnitIdentifierKey/MetadataName : nom de la balise utilisées pour le rattachement, récupérée dans le formulaire.
Management/UpdateOperation/ArchiveUnitIdentifierKey/MetadataValue : valeur fournie par l’utilisateur (premier élément du tuple « rattachement »).
Cette UA fantôme aura un élément Content/Title, dont la valeur sera retrouvée dans le formulaire, et un élément DescriptionLevel de type « RecordGrp », puisqu’elle correspond à un répertoire contenant l’ensemble des reportages ajoutés au SIP.


### 3.6.	Création des ArchiveUnit : niveaux imbriqués
La fonction sub_unit() gère la restitution de l’arborescence en imbriquant les ArchiveUnit de niveau inférieur les unes avec les autres avant de les restituer sous le niveau Reportage. Dans un premier temps, elle liste l’ensemble des fichiers et dossiers trouvés dans le chemin fourni (le dossier du reportage) et recrée le chemin de chacun de ces éléments. L’analyse du chemin permet de distinguer les dossiers des fichiers et d’apporter à chacun un traitement différent. 
Si l’élément est identifié comme un dossier, la fonction crée un élément ArchiveUnit et appelle la fonction create_archive_unit_dir() pour en renseigner les métadonnées au sein de l’élément Content. L’élément Content produit par cette fonction est ensuite ajouté à l’élément ArchiveUnit parent. Puis, la fonction sub_unit() est rappelée au sein de cette boucle pour s’appliquer au niveau inférieur. En bouclant ainsi sur elle-même, la fonction se répète autant de fois qu’il y a de niveaux de sous-dossiers, en restituant le niveau inférieur comme une ArchiveUnit enfant du niveau supérieur.
Si l’élément est identifié comme un fichier, la fonction vérifie d’abord qu’il ne s’agit pas d’un fichier système (en comparant son nom à une liste de noms de fichiers système identifiés pendant l’analyse des données). Puis, elle appelle la fonction create_archive_unit_file() qui crée un élément ArchiveUnit pour le fichier. Cet élément est ensuite ajouté à l’élément ArchiveUnit parent.
ArchiveUnit : sous-dossiers
La fonction create_archive_unit_dir() crée un élément Content et ses éléments enfant pour chaque sous- dossier au sein d’un reportage. Il reprend pour titre le nom du sous-dossier, les autres informations sont inscrites « en dur » dans le script (DescriptionLevel : « RecordGrp ») ou issues du formulaire  (OriginatingAgency/Identifier et SubmissionAgency/Identifier). 
ArchiveUnit : fichiers
La fonction create_archive_unit_file() crée un élément ArchiveUnit/Content par fichier. Au sein du Content sont ajoutées les métadonnées internes issues de l’extraction Exiftool.
Dans un premier temps, afin d’éviter les erreurs dues aux fichiers portant le même nom, la fonction utilise comme valeur pivot le chemin de fichier reconstitué dans la fonction précédente en le comparant avec celui créé par l’export Siegfried. Une fois que le bon fichier a été identifié, il s’agit uniquement de récupérer les métadonnées souhaitées et de les placer dans l’élément correspondant.
À chaque métadonnée, la fonction vérifie qu’elle existe bien pour ce fichier avant de créer l’élément. Ainsi, une photo n’ayant pas de légende n’aura pas de balise Description.
Lorsque plusieurs champs de métadonnées peuvent correspondre à une même information, un champ est utilisé en priorité. Par exemple, pour les mots-clés, l’application utilise en priorité les informations renseignées dans le champ XMP:Subject. Si ce champ est vide, nous interrogeons le champ IPTC:Keywords. Cette opération est répétée pour l’ensemble des métadonnées choisies (description, mots-clés, localisation, nom du photographe, date de création).
Lorsque l’identité du photographe est renseignée, deux métadonnées sont ajoutées automatiquement par l’application : les éléments Activity et Mandate, qui permettent de préciser la nature du droit exercé par l’AuthorizedAgent sur le fichier. Les valeurs de ces éléments sont issues du formulaire renseigné par l’utilisateur.
Un élément BaliseTemp est également créé : il contient l’empreinte du fichier associé à cette unité d’archive. Il ne s’agit pas d’un élément SEDA mais d’une balise temporaire (comme son nom l’indique), supprimée juste avant l’écriture du manifest, et qui permettra d’associer les DataObjectGroup aux bonnes ArchiveUnit.


### 3.7.	Suppression des doublons techniques
Il arrive que certains fichiers soient présents plusieurs fois au sein d’un versement. Afin de limiter la taille des versements, le SEDA permet de ne conserver qu’un seul de ces fichiers et de l’associer à plusieurs ArchiveUnit : ainsi, lors de la restitution, il sera recréé partout où il était présent dans l’arborescence, mais il ne sera conservé qu’une fois dans le SAE. 
La fonction delete_duplicate_dog() a justement pour objectif de supprimer les DataObjectGroup correspondant à des doublons techniques. Elle parcourt l’ensemble des DataObjectGroup et en mémorise l’empreinte. Celle-ci est ensuite ajoutée à une liste « à conserver ». Si l’empreinte est déjà présente dans la liste, cela signifie donc qu’il s’agit d’un doublon : le DataObjectGroup correspondant au doublon est ajouté à une seconde liste « suppressions  ». À l’issue de son parcours, la fonction supprime de l’arbre XML les DataObjectGroup présents dans la liste « suppressions ».


### 3.8.	Attribution des identifiants
La fonction id_attrib() parcourt un manifest presque terminé pour associer à chaque ArchiveUnit et chaque DataObjectGroup les identifiants qui permettront d’assurer les liens entre unités d’archives, fichiers et groupes d’objets techniques. 
Pour chaque DataObjectGroup, BinaryDataObject et ArchiveUnit, elle attribue un identifiant de manière incrémentale (GOT1, GOT2, GOT3… / BDO1, BDO2, BDO3… / AU1, AU2, AU3…). 
En se basant sur la valeur de l’élément DescriptionLevel de chaque ArchiveUnit, la fonction détermine s’il s’agit d’un fichier ou d’un dossier. Pour chaque fichier, elle compare l’empreinte contenue dans l’élément BaliseTemp aux empreintes de BinaryDataObject. L’élément DataObjectGroupReferenceId de l’ArchiveUnit prend ensuite pour valeur l’identifiant du BinaryDataObject correspondant.


### 3.9.	Création du ManagementMetadata
L’élément ManagementMetadata associé à l’ensemble du SIP doit se situer en dernière position parmi les enfants du DataObjectPackage. Il contient un ensemble de métadonnées de gestion propres à ce versement qui sont renseignées par l’utilisateur dans le formulaire.
La fonction create_management_metadata() étant la dernière à modifier le manifest, après la création de l’élément ManagementMetadata, elle est également chargée de la suppression de l’ensemble des éléments temporaires BaliseTemp créés dans les Archive Unit.


### 3.10.	Copie et renommage des fichiers
La fonction copy() crée un chemin de destination pour chaque fichier composé de  : 
*	Le chemin vers le dossier parent  ;
*	La valeur de l’attribut «  id  » de chaque BinaryDataObject  ;
*	L’extension issue du nom du fichier (.jpg).
Elle récupère ensuite le chemin originel de chaque fichier tel qu’il apparait dans l’export Siegfried. Grâace à la fonction copy du module shutil, ces deux informations (ancien chemin, nouveau chemin) suffisent à copier et renommer les fichiers.
L’identification se fait à partir du manifest et non à partir du contenu du dossier pour éviter l’ajout de fichiers non retenus lors de la reprise des données (fichiers système, fichiers raw, etc).
