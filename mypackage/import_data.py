import os
import csv
from exiftool import ExifTool
import subprocess
import json
import sys


def select_list_rp(liste_rp):
    """
    Sélectionne le fichier texte contenant les numéros des reportages à ajouter au SIP.

    :return: list - la liste des numéros des reportages à analyser.
    """
    list_rp = liste_rp
    my_file = open(list_rp, "r")
    data = my_file.read()
    # Fichier texte transformé en liste en transformant chaque retour à la ligne en virgule
    data_into_list = data.replace('\n', ',').split(",")
    return data_into_list


def select_csv(csv_file):
    """
    Sélectionne le csv contenant les métadonnées externes des reportages.

    :return: list[list] - le contenu du csv de métadonnées.
    """
    csv_path = csv_file
    data_ir = []
    with open(csv_path, encoding="utf-8", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data_ir.append(row)
    return data_ir


def chose_target_dir(cible_dir):
    """
    Sélectionne le répertoire où sera créé le SIP.

    :return: str - le chemin du répertoire de destination.
    """
    target_dir = cible_dir
    content = 'content'
    path = os.path.join(target_dir, content)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def exif_extract(dir_path, liste_rp, formulaire):
    """
    Utilise la librairie PyExiftool pour extraire les métadonnées internes des photos.
    :param str dir_path: le chemin vers le répertoire "racine" contenant les reportages.
    :param list liste_rp: la liste des numéros des reportages à ajouter au SIP.

    :return: list[dict] - une liste de dictionnaires, chaque dictionnaire contenant les métadonnées extraites
    pour un fichier.
    """
    data = []  # Initialisation de la liste qui va contenir les métadonnées extraites
    processed_files = set()  # Pour garder une trace des fichiers déjà traités
    # Utilisation de PyExiftool pour extraire les métadonnées internes des photographies
    with ExifTool(encoding="utf-8") as et:
        for rp in liste_rp:  # Parcours de chaque numéro de reportage dans la liste
            # Si un numéro de reportage de la liste n'est pas identifié dans les noms de dossier, interrompre le script
            if rp.lower() not in str(os.listdir(dir_path)).lower():
                input("ERREUR : Le reportage " + rp + " n'a pas été trouvé dans le répertoire "+dir_path+".")
                sys.exit("ANNULATION")
            for item in os.listdir(dir_path):  # Parcours de chaque élément dans le répertoire racine
                # Vérification si le nom de dossier contient un numéro de reportage
                if str(rp+" ").lower() in item.lower() or item.lower().endswith(rp.lower()) or str(rp+"_").lower() in item.lower():
                    item_path = os.path.join(dir_path, item)  # Chemin complet vers le dossier ou fichier
                    # Extraction des métadonnées spécifiques pour les fichiers du dossier
                    exif_data_list = et.execute_json(
                        '-r', '-b', '-FileName', *formulaire["Champs_metadata"], '-Filesize#', item_path
                    )
                    # Vérification si le fichier a déjà été traité pour éviter les doublons
                    if item_path in processed_files:
                        continue  # Passer au prochain fichier si celui-ci a déjà été traité
                        # Si des métadonnées sont extraites, les ajouter à la liste des données
                    if exif_data_list:
                        data.extend(exif_data_list)
                        processed_files.add(item_path)  # Ajouter le fichier à la liste des fichiers traités
    return data  # Retourner la liste des métadonnées extraites pour tous les fichiers concernés


def siegfried(dir_path, liste_rp):
    """
    Utilise l'outil Siegfried pour extraire les métadonnées de format des fichiers.
    :param str dir_path: le chemin vers le répertoire "racine" contenant les reportages.
    :param list liste_rp: la liste des numéros des reportages à analyser.

    :return: list[dict] - une liste de dictionnaires contenant les métadonnées de format des fichiers.
    """
    format_rp = []  # Liste qui va contenir les métadonnées de format des fichiers par reportage
    # Parcours de chaque numéro de reportage dans la liste
    for rp in liste_rp:
        # Parcours de chaque élément (fichier ou dossier) dans le répertoire racine
        for item in os.listdir(dir_path):
            if str(rp+" ").lower() in item.lower() or item.lower().endswith(rp.lower()):
                item_path = os.path.join(dir_path, item)  # Chemin complet vers le dossier ou fichier
                # Appel à Siegfried pour obtenir les métadonnées de format au format JSON
                md_format = subprocess.run(["sf", "-hash", "sha512", "-json", item_path], capture_output=True,
                                           text=True, encoding="utf-8")
                md_format = json.loads(md_format.stdout)  # Conversion de la sortie JSON en dictionnaire Python
                format_rp.append(md_format)  # Ajouter le fichier à la liste des fichiers traités
                # Ajout des métadonnées de format pour ce reportage à la liste

    # Correction des chemins de fichier dans chaque dictionnaire de métadonnées de format
    for rp in format_rp:
        fichiers = rp.get("files", [])   # Récupération de la liste des fichiers dans les métadonnées du reportage
        for file in fichiers:
            # Remplacement des séparateurs de chemin Windows par des slashs
            file["filename"] = file["filename"].replace("\\", "/")

    return format_rp  # Retourne la liste de dictionnaires contenant les métadonnées de format des reportages analysés


def metadata_json(data_sig, data_exif):
    """
    Fusionne les métadonnées des fichiers provenant de deux sources de données.
    :param list data_sig: liste de dictionnaires contenant des métadonnées calculées par Siegfried, chacun avec une clé
    "files" qui est une liste de fichiers.
    :param list data_exif: liste de dictionnaires contenant des métadonnées extraites par Exiftool, chacun avec une clé
    "SourceFile" indiquant le chemin du fichier.

    :return: list[dict] - une nouvelle liste de dictionnaires avec les métadonnées fusionnées pour chaque fichier.
    """
    new_data = []  # Initialisation d'une liste vide pour stocker les données fusionnées

    # Parcours de chaque reportage dans les données de Siegfried
    for rp in data_sig:
        files = rp.get("files", [])  # Récupération de la liste des fichiers pour ce reportage

        # Parcours de chaque fichier dans le reportage
        for file in files:
            filename = file["filename"]  # Extraction du nom du fichier
            # Recherche correspondante dans les métadonnées extraites par Exiftool
            for item in data_exif:
                if item.get("SourceFile") == filename:
                    file.update(item)  # Mise à jour des métadonnées du fichier avec celles de Exiftool

        # Ajout du reportage avec les fichiers fusionnés à la liste finale
        new_data.append({'files': files})

    return new_data  # Retourne une liste de dictionnaires avec les métadonnées fusionnées pour tous les fichiers

