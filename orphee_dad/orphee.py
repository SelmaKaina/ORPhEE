import os
from datetime import datetime
import xml.etree.ElementTree as ET
from tkinter import filedialog
import csv
from exiftool import ExifTool
import re
import subprocess
import json
import shutil
import sys
from xml.dom import minidom


# -*- coding: utf-8 -*-

# Import de la date du jour de fabrication du SIP
date_ajd = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")


def get_archiveunit_id():
    """
    Demande à l'utilisateur le numéro d'entrée du paquet d'archives.

    :return: str - le numéro d'entrée.
    """
    num_entree = input("Saisissez le numéro d'entrée : ")
    num_paquet = input("Saisissez le numéro du paquet : ")
    archival_agency_archive_unit_identifier = num_entree + "_" + num_paquet + "_"
    return archival_agency_archive_unit_identifier


def updateoperation():
    """
    Demande à l'utilisateur s'il souhaite rattacher le paquet d'archives à une unité archivistique déjà versée.

    :return: list - les valeurs des balises <ArchivalAgencyArchiveUnitIdentifier> et <Title> de l'UA de rattachement.
    """
    user_input = input("Voulez-vous rattacher ce paquet à une autre unité archivistique ? (Oui/Non): ")
    if user_input.lower() in ["oui", "o"]:
        ua = input("Saisissez la valeur de la balise 'ArchivalAgencyArchiveUnitIdentifier' de l'UA de rattachement : ")
        titre = input("Saisissez la valeur de la balise <Title> de l'UA de rattachement : ")
        return [ua, titre]
    else:
        print("D'accord, passons à la suite...")


def comment_message_id():
    """
    Demande à l'utilisateur la valeur qu'il souhaite faire apparaître dans les balises <Comment> et
    <MessageIdentifier> dans l'en-tête du manifest.

    :return: str - la valeur des balises <Comment> et <MessageIdentifier>.
    """
    value = input("Saisissez la valeur des balises Comment et MessageIdentifier :")
    return value


def select_list_rp():
    """
    Sélectionne le fichier texte contenant les numéros des reportages à ajouter au SIP.

    :return: list - la liste des numéros des reportages à analyser.
    """
    input("Appuyez sur Entrée pour sélectionner le fichier txt contenant la liste des reportages à ajouter au paquet.")
    list_rp = filedialog.askopenfilename()
    my_file = open(list_rp, "r")
    data = my_file.read()
    # Fichier texte transformé en liste en transformant chaque retour à la ligne en virgule
    data_into_list = data.replace('\n', ',').split(",")
    return data_into_list


def select_directory():
    """
    Sélectionne le répertoire contenant dossiers à ajouter au SIP.

    :return: str - le chemin du répertoire "racine" contenant les dossiers.
    """
    input("Appuyez sur Entrée pour sélectionner le dossier contenant les reportages à ajouter au paquet.")
    dir_path = filedialog.askdirectory()
    print(dir_path)
    return dir_path


def select_csv():
    """
    Sélectionne le csv contenant les métadonnées externes des reportages.

    :return: list[list] - le contenu du csv de métadonnées.
    """
    input("Appuyez sur Entrée pour sélectionner le fichier csv de métadonnées externes.")
    csv_path = filedialog.askopenfilename()
    data_ir = []
    with open(csv_path, encoding="utf-8", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            data_ir.append(row)
    return data_ir


def chose_target_dir():
    """
    Sélectionne le répertoire où sera créé le SIP.

    :return: str - le chemin du répertoire de destination.
    """
    input("Appuyez sur Entrée pour sélectionner le dossier de destination.")
    target_dir = filedialog.askdirectory()
    content = 'content'
    path = os.path.join(target_dir, content)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def exif_extract(dir_path, liste_rp):
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
                if (
                        str(rp+" ").lower() in item.lower() or item.lower().endswith(rp.lower()) or
                        str(rp+"_").lower() in item.lower()
                ):
                    item_path = os.path.join(dir_path, item)  # Chemin complet vers le dossier ou fichier
                    # Extraction des métadonnées spécifiques pour les fichiers du dossier
                    exif_data_list = et.execute_json(
                        '-r', '-b', '-FileName', '-CreateDate', '-By-line', '-Artist', '-City', '-Country',
                        '-Country-PrimaryLocationName', '-Description', '-Subject', '-Keywords', '-FileModifyDate',
                        '-Filesize#', item_path
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
            if (
                    str(rp+" ").lower() in item.lower() or item.lower().endswith(rp.lower()) or
                    str(rp+"_").lower() in item.lower()
            ):
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


def creer_root(value):
    """
    Crée l'élément XML racine et l'en-tête du manifest.

    :param str value: la valeur textuelle des balises <Comment> et <Message Identifier>.
    :return: xml.etree.ElementTree.Element - l'élément racine XML créé.
    """
    root = ET.Element("ArchiveTransfer")  # Création de l'élément racine XML 'ArchiveTransfer'

    # Définition des espaces de noms et de l'emplacement du schéma XML
    root.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
    root.set('xmlns:pr', 'info:lc/xmlns/premis-v2')
    root.set('xmlns', 'fr:gouv:culture:archivesdefrance:seda:v2.1')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation', 'fr:gouv:culture:archivesdefrance:seda:v2.1 seda-2.1-main.xsd')
    root.set('xml:id', 'ID1')   # Attribution de l'identifiant XML 'ID1'

    # Ajout de l'élément 'Comment' avec la valeur spécifiée
    comment = ET.SubElement(root, "Comment")
    comment.text = value
    # Ajout de l'élément 'Date' avec la date du jour de fabrication du SIP
    date = ET.SubElement(root, "Date")
    date.text = date_ajd

    # Ajout de l'élément 'MessageIdentifier' avec la valeur spécifiée
    ET.SubElement(root, "MessageIdentifier").text = value

    # Ajout de l'élément 'ArchivalAgreement' avec sa valeur et ses espaces de noms
    archag = ET.SubElement(root, "ArchivalAgreement")
    archag.text = "FRAN_CE_0001"
    archag.set('xmlns', 'fr:gouv:culture:archivesdefrance:seda:v2.1')
    archag.set('xmlns:ns2', 'http://www.w3.org/1999/xlink')

    # Ajout de l'élément 'CodeListVersions' avec ses sous-éléments et leurs valeurs
    codelist = ET.SubElement(root, "CodeListVersions")
    codelist.set('xmlns', 'fr:gouv:culture:archivesdefrance:seda:v2.1')
    codelist.set('xmlns:ns2', 'http://www.w3.org/1999/xlink')
    ET.SubElement(codelist, "ReplyCodeListVersion").text = "ReplyCodeListVersion0"
    ET.SubElement(codelist, "MessageDigestAlgorithmCodeListVersion").text = "MessageDigestAlgorithmCodeListVersion0"
    ET.SubElement(codelist, "MimeTypeCodeListVersion").text = "MimeTypeCodeListVersion0"
    ET.SubElement(codelist, "EncodingCodeListVersion").text = "EncodingCodeListVersion0"
    ET.SubElement(codelist, "FileFormatCodeListVersion").text = "FileFormatCodeListVersion0"
    ET.SubElement(codelist, "CompressionAlgorithmCodeListVersion").text = "CompressionAlgorithmCodeListVersion0"
    ET.SubElement(codelist, "DataObjectVersionCodeListVersion").text = "DataObjectVersionCodeListVersion0"
    ET.SubElement(codelist, "StorageRuleCodeListVersion").text = "StorageRuleCodeListVersion0"
    ET.SubElement(codelist, "AppraisalRuleCodeListVersion").text = "AppraisalRuleCodeListVersion0"
    ET.SubElement(codelist, "AccessRuleCodeListVersion").text = "AccessRuleCodeListVersion0"
    ET.SubElement(codelist, "DisseminationRuleCodeListVersion").text = "DisseminationRuleCodeListVersion0"
    ET.SubElement(codelist, "ReuseRuleCodeListVersion").text = "ReuseRuleCodeListVersion0"
    ET.SubElement(codelist, "ClassificationRuleCodeListVersion").text = "ClassificationRuleCodeListVersion0"
    ET.SubElement(codelist, "AuthorizationReasonCodeListVersion").text = "AuthorizationReasonCodeListVersion0"
    ET.SubElement(codelist, "RelationshipCodeListVersion").text = "RelationshipCodeListVersion0"

    # Ajout de l'élément 'DataObjectPackage'
    ET.SubElement(root, "DataObjectPackage")

    # Ajout de l'élément 'TransferRequestReplyIdentifier' avec sa valeur
    ET.SubElement(root, "TransferRequestReplyIdentifier").text = "Identifier3"

    # Ajout de l'élément 'ArchivalAgency' avec son identifiant
    archival_agency = ET.SubElement(root, "ArchivalAgency")
    ET.SubElement(archival_agency, "Identifier").text = "Archives nationales"

    # Ajout de l'élément 'TransferringAgency' avec son identifiant et ses espaces de noms
    transferring_agency = ET.SubElement(root, "TransferringAgency")
    transferring_agency.set('xmlns', 'fr:gouv:culture:archivesdefrance:seda:v2.1')
    transferring_agency.set('xmlns:ns2', 'http://www.w3.org/1999/xlink')
    ET.SubElement(transferring_agency, "Identifier").text = "Mission Présidence de la République"

    return root  # Retourne l'élément racine XML créé


def create_dataobjectgroup(arbre, directory, liste_rp):
    """
        Crée l'élément <DataObjectPackage> et un élément <DataObjectGroup> pour chaque fichier correspondant aux
        reportages spécifiés.

        :param ElementTree Element arbre: L'élément racine de l'arbre XML.
        :param str directory: Le chemin vers le répertoire racine contenant les dossiers des reportages.
        :param list liste_rp: La liste des numéros des reportages à inclure dans le SIP.

        :return: ElementTree Element - l'élément racine XML mis à jour avec les groupes d'objets techniques ajoutés.
        """
    root = arbre  # Utilisation de l'arbre XML passé en paramètre comme racine

    # Recherche de l'élément DataObjectPackage dans l'arbre XML
    data_object_package = root.find("DataObjectPackage")

    # Parcours récursif de tous les fichiers et répertoires dans le répertoire spécifié
    for dirpath, dirnames, filenames in os.walk(directory):
        # Remplacement des antislashs pour compatibilité avec les chemins
        dirpath = dirpath.replace("\\", "/")
        for i in filenames:
            item = dirpath + "/" + i  # Chemin complet du fichier
            for num in liste_rp:
                # Vérification si le numéro de reportage est dans le chemin du fichier
                if (
                        str(num+" ").lower() in item.lower() or str(num+"/").lower() in item.lower() or
                        str(num+"_").lower() in item.lower()
                ):
                    # Exclusions de certains fichiers non pertinents (fichiers système ou masqués)
                    if (
                            "DS_Store" not in item and "Thumbs" not in item and "BridgeSort" not in item and
                            "PM_lock" not in item and "desktop.ini" not in item and
                            "._" not in item and "/." not in item
                    ):
                        # Création de l'élément DataObjectGroup sous DataObjectPackage et de ses descendants
                        data_object_group = ET.SubElement(data_object_package, "DataObjectGroup")
                        binary_data_object = ET.SubElement(data_object_group, "BinaryDataObject")
                        ET.SubElement(binary_data_object, "DataObjectVersion").text = "BinaryMaster_1"
                        ET.SubElement(binary_data_object, "Uri")
                        message_digest = ET.SubElement(binary_data_object, "MessageDigest")
                        message_digest.set("algorithm", "SHA-512")
                        ET.SubElement(binary_data_object, "Size")
                        format_identification = ET.SubElement(binary_data_object, "FormatIdentification")
                        ET.SubElement(format_identification, "FormatLitteral")
                        file_info = ET.SubElement(binary_data_object, "FileInfo")
                        filename = ET.SubElement(file_info, "Filename")
                        filename.text = item  # Création de l'élément Filename avec pour valeur le nom du fichier
                        ET.SubElement(file_info, "LastModified")

    return root  # Retourne l'élément racine XML mis à jour avec les nouveaux groupes d'objets de données


def package_metadata(arbre, data):
    """
    Complète les métadonnées des objets techniques dans l'arbre XML avec les informations fournies dans data.

    :param xml.etree.ElementTree.Element arbre: L'élément racine de l'arbre XML à mettre à jour.
    :param list[dict] data: Une liste de dictionnaires contenant les métadonnées des fichiers (fusion des exports
    Siegfried et Exiftool).

    :return: ElementTree Element - l'élément racine XML mis à jour avec les métadonnées des objets techniques.
    """
    root = arbre  # Utilisation de l'arbre XML passé en paramètre comme racine

    # Recherche de l'élément DataObjectPackage dans l'arbre XML
    data_object_package = root.find("DataObjectPackage")
    # Recherche de tous les éléments BinaryDataObject sous DataObjectPackage
    binary_data_object = data_object_package.findall(".//BinaryDataObject")

    # Parcours de chaque BinaryDataObject
    for obj in binary_data_object:
        item = obj.find(".//Filename").text  # Récupération du nom de fichier

        # Parcours des données fournies (fusion des exports Siegfried et Exiftool)
        for rp in data:
            files = rp.get("files", [])  # Récupération des fichiers et leurs métadonnées
            for file in files:
                if file.get("filename") == item:  # Vérification si le fichier correspond à l'objet actuel
                    # Mise à jour des métadonnées dans l'élément XML
                    if file.get("File:FileSize"):
                        filesize = obj.find("Size")
                        filesize.text = str(file["File:FileSize"])  # Mise à jour de la taille du fichier

                    if file.get("File:FileModifyDate"):
                        last_modified = obj.find(".//LastModified")
                        modif_date = file.get("File:FileModifyDate")  # Récupération de la date de dernière modification
                        # Extraction de la date au format attendu
                        match = re.match(r"(\d{4}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2})(\\.\d+)?([-+]\d{2}:\d{2})?",
                                         modif_date)
                        if match:
                            modif_date = match.group(1)
                            # Conversion de la date en format ISO 8601
                            modif_date = datetime.strptime(modif_date, "%Y:%m:%d %H:%M:%S")
                            modif_date = modif_date.strftime("%Y-%m-%dT%H:%M:%S")
                            last_modified.text = modif_date

                    # Mise à jour du nom de fichier
                    file_name = obj.find(".//Filename")
                    file_name.text = file.get("File:FileName")

                    # Mise à jour des éléments d'identification du format
                    message_digest = obj.find("MessageDigest")
                    message_digest.text = file.get("sha512")
                    format_identification = obj.find("FormatIdentification")
                    format_litteral = format_identification.find("FormatLitteral")
                    for i in file.get("matches"):
                        format_litteral.text = i["format"]  # Mise à jour du format littéral
                        if i["mime"]:
                            ET.SubElement(format_identification, "MimeType").text = i["mime"]  # Ajout du type mime
                        formatid = ET.SubElement(format_identification, "FormatId")
                        formatid.text = i["id"]  # Mise à jour de l'ID de format

    return root  # Retourne l'élément racine XML mis à jour avec les métadonnées des objets techniques


def ua_rp(directory, data_ir, arbre_rp, data, liste_rp, rattachement):
    """
    Crée des unités d'archive pour chaque reportage et appelle la fonction sub_unit() pour les UA de niveau inférieur,
    puis les ajoute à l'arbre XML.

    :param str directory: le chemin du répertoire contenant les reportages.
    :param list[list] data_ir: une liste de liste, chacune contenant les métadonnées externes d'un reportage.
    :param xml.etree.ElementTree.Element arbre_rp: l'arbre XML mis à jour.
    :param list[dict] data: une liste de dictionnaires contenant les métadonnées des fichiers (fusion des exports
    Siegfried et Exiftool).
    :param list liste_rp: une liste des numéros des reportages à ajouter au SIP.
    :param list rattachement: une liste contenant les informations de rattachement, ou None.

    :return: xml.etree.ElementTree.Element - l'élément racine XML mis à jour.
    """
    root = arbre_rp  # Utilisation de l'arbre XML passé en paramètre comme racine
    data_object_package = root.find("DataObjectPackage")  # Recherche de l'élément DataObjectPackage

    # Création de l'élément DescriptiveMetadata sous DataObjectPackage s'il n'existe pas déjà
    descriptive_metadata = ET.SubElement(data_object_package, "DescriptiveMetadata")
    if rattachement is not None:
        # Si des informations de rattachement sont fournies, créer une unité d'archive "fantôme"
        ua_ghost = ET.Element("ArchiveUnit")  # Création de l'élément ArchiveUnit
        management = ET.SubElement(ua_ghost, "Management")  # Sous-élément Management de ArchiveUnit
        update_operation = ET.SubElement(management, "UpdateOperation")  # Sous-élément UpdateOperation de Management
        archive_unit_identifier_key = ET.SubElement(update_operation, "ArchiveUnitIdentifierKey")
        metadata_name = ET.SubElement(archive_unit_identifier_key, "MetadataName")
        metadata_name.text = "ArchivalAgencyArchiveUnitIdentifier"  # Valeur de MetadataName
        metadata_value = ET.SubElement(archive_unit_identifier_key, "MetadataValue")
        metadata_value.text = rattachement[0]  # Valeur de MetadataValue issue de la liste "rattachement"
        content_ghost = ET.SubElement(ua_ghost, "Content")  # Sous-élément Content de ArchiveUnit
        ET.SubElement(content_ghost, "DescriptionLevel").text = "RecordGrp"  # Valeur de DescriptionLevel
        title_ghost = ET.SubElement(content_ghost, "Title")
        title_ghost.text = rattachement[1]  # Valeur de Title issue de la liste "rattachement"

        # Parcours des fichiers dans le répertoire spécifié
        for num in liste_rp:
            for item in os.listdir(directory):
                for RP in data_ir:
                    if num == RP[0]:
                        if (
                                str(num+" ").lower() in item.lower() or item.lower().endswith(num.lower()) or
                                str(num+"_").lower() in item.lower()
                        ):
                            print(num)  # Affichage du nom du fichier pour vérification
                            item_path = os.path.join(directory, item)
                            if os.path.isdir(item_path):
                                # Création d'une nouvelle unité d'archive pour chaque reportage
                                archiveunitrp = ET.SubElement(ua_ghost, "ArchiveUnit")
                                contentrp = ET.SubElement(archiveunitrp, "Content")
                                ET.SubElement(contentrp, "DescriptionLevel").text = "RecordGrp"
                                titlerp = ET.SubElement(contentrp, "Title")
                                titlerp.text = RP[1]  # Titre du reportage issu du csv de métadonnées externes
                                ET.SubElement(contentrp, "ArchivalAgencyArchiveUnitIdentifier")
                                numrp = ET.SubElement(contentrp, "OriginatingAgencyArchiveUnitIdentifier")
                                numrp.text = RP[0]  # Identifiant du reportage issu du csv de métadonnées externes
                                if len(RP) > 4:
                                    if RP[4]:
                                        cote = ET.SubElement(contentrp, "TransferringAgencyArchiveUnitIdentifier")
                                        cote.text = RP[4]
                                description = ET.SubElement(contentrp, "Description")
                                # Numéro du reportage en description (pour indexation dans le SAE)
                                description.text = str("Reportage n°"+RP[0])
                                # Identifiant du service producteur et versant
                                originating_agency = ET.SubElement(contentrp, "OriginatingAgency")
                                ET.SubElement(originating_agency, "Identifier").text = "FRAN_NP_009886"
                                submission_agency = ET.SubElement(contentrp, "SubmissionAgency")
                                ET.SubElement(submission_agency, "Identifier").text = "FRAN_NP_009886"
                                startdate = ET.SubElement(contentrp, "StartDate")
                                if RP[2] is not None:
                                    dtd = datetime.strptime(RP[2], "%d.%m.%Y")
                                    dtd = dtd.strftime("%Y-%m-%dT%H:%M:%S")
                                    startdate.text = dtd  # Date de début du reportage issue du csv
                                else:
                                    startdate.text = "0000-00-00T00:00:00"
                                enddate = ET.SubElement(contentrp, "EndDate")
                                if RP[3] is not None:
                                    dtf = datetime.strptime(RP[3], "%d.%m.%Y")
                                    dtf = dtf.strftime("%Y-%m-%dT%H:%M:%S")
                                    enddate.text = dtf  # Date de fin du reportage issue du csv de métadonnées externes
                                else:
                                    enddate.text = "0000-00-00T00:00:00"

                                # Appel à la fonction sub_unit pour les sous-unités d'archive
                                archiveunitchild = sub_unit(item_path, data, data_ir, liste_rp)
                                for child in archiveunitchild:
                                    # Ajout des sous-unités d'archive à l'unité d'archive parente
                                    archiveunitrp.append(child)

        descriptive_metadata.append(ua_ghost)  # Ajout de l'unité d'archive "fantôme" à DescriptiveMetadata

    else:
        # Si aucune information de rattachement n'est fournie, procéder de manière similaire sans UA "fantôme"
        for num in liste_rp:
            for item in os.listdir(directory):
                for RP in data_ir:
                    if num == RP[0]:
                        if (
                                str(num+" ").lower() in item.lower() or item.lower().endswith(num.lower()) or
                                str(num+"_").lower() in item.lower()
                        ):
                            print(num)  # Affichage du nom du fichier pour vérification
                            item_path = os.path.join(directory, item)
                            if os.path.isdir(item_path):
                                # Création d'une nouvelle unité d'archive pour chaque reportage
                                archiveunitrp = ET.Element("ArchiveUnit")
                                contentrp = ET.SubElement(archiveunitrp, "Content")
                                ET.SubElement(contentrp, "DescriptionLevel").text = "RecordGrp"
                                titlerp = ET.SubElement(contentrp, "Title")
                                titlerp.text = RP[1]  # Titre du reportage issu du csv de métadonnées externes
                                ET.SubElement(contentrp, "ArchivalAgencyArchiveUnitIdentifier")
                                numrp = ET.SubElement(contentrp, "OriginatingAgencyArchiveUnitIdentifier")
                                numrp.text = RP[0]  # Identifiant du reportage issu du csv de métadonnées externes
                                if len(RP) > 4:
                                    if RP[4]:
                                        cote = ET.SubElement(contentrp, "TransferringAgencyArchiveUnitIdentifier")
                                        cote.text = RP[4]
                                description = ET.SubElement(contentrp, "Description")
                                # Numéro du reportage en description (pour indexation dans le SAE)
                                description.text = str("Reportage n°"+RP[0])
                                # Identifiant du service producteur et versant
                                originating_agency = ET.SubElement(contentrp, "OriginatingAgency")
                                ET.SubElement(originating_agency, "Identifier").text = "FRAN_NP_009886"
                                submission_agency = ET.SubElement(contentrp, "SubmissionAgency")
                                ET.SubElement(submission_agency, "Identifier").text = "FRAN_NP_009886"
                                startdate = ET.SubElement(contentrp, "StartDate")
                                if RP[2] is not None:
                                    dtd = datetime.strptime(RP[2], "%d.%m.%Y")
                                    dtd = dtd.strftime("%Y-%m-%dT%H:%M:%S")
                                    startdate.text = dtd  # Date de début du reportage issue du csv
                                else:
                                    startdate.text = "0000-00-00T00:00:00"
                                enddate = ET.SubElement(contentrp, "EndDate")
                                if RP[3] is not None:
                                    dtf = datetime.strptime(RP[3], "%d.%m.%Y")
                                    dtf = dtf.strftime("%Y-%m-%dT%H:%M:%S")
                                    enddate.text = dtf  # Date de fin du reportage issue du csv de métadonnées externes
                                else:
                                    enddate.text = "0000-00-00T00:00:00"

                                # Appel à la fonction sub_unit pour les sous-unités d'archive
                                archiveunitchild = sub_unit(item_path, data, data_ir, liste_rp)
                                for child in archiveunitchild:
                                    archiveunitrp.append(child)
                                # Ajout des sous-unités d'archive à l'unité d'archive parente

                                # Ajout de l'unité d'archive à DescriptiveMetadata
                                descriptive_metadata.append(archiveunitrp)

    return root  # Retour de l'arbre XML mis à jour avec les unités d'archive


def sub_unit(directory, data, data_ir, liste_rp, parent=None):
    """
    Crée des unités d'archive pour les fichiers en appelant la fonction et sous-répertoires dans le répertoire spécifié,
    et les ajoute à l'unité d'archive parente.

    :param str directory: Le chemin du répertoire contenant les fichiers et sous-répertoires.
    :param list[dict] data: Une liste de dictionnaires contenant les métadonnées des fichiers (fusion des exports
    Siegfried et Exiftool).
    :param list[list] data_ir: Une liste de liste, chacune contenant les métadonnées externes d'un reportage.
    :param list liste_rp: Une liste des numéros des reportages à traiter.
    :param xml.etree.ElementTree.Element parent: L'unité d'archive parente à laquelle ajouter les sous-unités, ou None
    pour créer une nouvelle unité d'archive racine.

    :return: Liste - une liste des sous-unités d'archive
    """
    if parent is None:
        archiveunit = ET.Element("ArchiveUnit")  # Création de l'élément ArchiveUnit
    else:
        archiveunit = parent

    # Parcours des éléments (fichiers et sous-répertoires) dans le répertoire spécifié
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            if item.startswith('.'):
                pass
            else:
                # Si l'élément est un répertoire, créer une sous-unité d'archive
                sub_archive_unit = ET.SubElement(archiveunit, "ArchiveUnit")
                contentsub = create_archive_unit_dir(item)
                sub_archive_unit.append(contentsub)
                # Appel récursif de la fonction pour traiter les sous-répertoires
                sub_unit(item_path, data, data_ir, liste_rp, sub_archive_unit)

        elif (
                os.path.isfile(item_path) and "DS_Store" not in item and "Thumbs" not in item and
                "BridgeSort" not in item and "desktop.ini" not in item
        ):
            # Si l'élément est un fichier valide (et non un fichier système)
            if item.startswith('.'):
                pass
            else:
                file_unit = create_archive_unit_file(item, data, item_path)
                archiveunit.append(file_unit)  # Ajout de l'unité d'archive du fichier à l'unité d'archive parent

    # Si aucune unité d'archive parent n'a été fournie, retourner les sous-unités d'archive créées
    if parent is None:
        au_child = archiveunit.findall("./ArchiveUnit")
        return au_child


def create_archive_unit_dir(title_dir):
    """
    Crée le contenu d'une unité d'archive pour un répertoire.

    :param str title_dir: le titre du répertoire à utiliser comme titre de l'unité d'archive.

    :return: xml.etree.ElementTree.Element - un élément XML représentant le contenu de l'unité d'archive pour le
    répertoire.
    """
    # Création d'un élément Content contenant les métadonnées relatives au sous-dossier
    contentdir = ET.Element("Content")
    ET.SubElement(contentdir, "DescriptionLevel").text = "RecordGrp"
    title_element = ET.SubElement(contentdir, "Title")
    title_element.text = title_dir  # Titre du sous-dossier
    ET.SubElement(contentdir, "ArchivalAgencyArchiveUnitIdentifier")
    originating_agency = ET.SubElement(contentdir, "OriginatingAgency")
    ET.SubElement(originating_agency, "Identifier").text = "FRAN_NP_009886"  # Identifiant du service producteur
    submission_agency = ET.SubElement(contentdir, "SubmissionAgency")
    ET.SubElement(submission_agency, "Identifier").text = "FRAN_NP_009886"  # Identifiant du service versant

    return contentdir  # Retourner le Content créé pour l'ajouter à l'UA correspondante, crée par la fonction sub_unit()


def create_archive_unit_file(title_file, data, item_path):
    """
    Crée un élément ArchiveUnit pour représenter les métadonnées d'un fichier.

    :param str title_file: Le nom du fichier.
    :param list[dict] data: une liste de dictionnaires contenant les métadonnées des fichiers (fusion des exports
    Siegfried et Exiftool).
    :param str item_path: Le chemin complet du fichier.

    :return: xml.etree.ElementTree.Element - L'élément XML ArchiveUnit et ses descendants, contenant les métadonnées du
    fichier.
    """
    # Remplace les backslashes par des slashes dans le chemin du fichier (pour compatibilité système)
    item_path = item_path.replace("\\", "/")

    # Crée l'élément principal ArchiveUnit
    arch_unit_item = ET.Element("ArchiveUnit")
    # Crée le sous-élément Content
    contentit = ET.SubElement(arch_unit_item, "Content")
    # Ajoute le niveau de description de l'élément
    ET.SubElement(contentit, "DescriptionLevel").text = "Item"
    # Ajoute le titre du fichier
    title_element = ET.SubElement(contentit, "Title")
    title_element.text = title_file
    # Ajoute un identifiant d'archive (complété plus tard)
    ET.SubElement(contentit, "ArchivalAgencyArchiveUnitIdentifier")

    # Parcourt les métadonnées fournies pour trouver celles correspondant au fichier actuel
    for item in data:
        files = item.get("files", [])
        for file in files:
            sourcefile = file.get("SourceFile")
            if sourcefile == item_path:
                # Ajoute les métadonnées spécifiques au fichier si elles n'existent pas déjà dans l'élément
                if contentit.find("BaliseTemp") is None:
                    # Ajout d'un élément temporaire BaliseTemp qui permettra d'identifier les doublons techniques
                    temp_hash = ET.SubElement(contentit, "BaliseTemp")
                    temp_hash.text = file.get("sha512")

                # Ajout d'un élément Description si une description existe dans les métadonnées internes du fichier
                if contentit.find("Description") is None:
                    if file.get("IPTC:Caption-Abstract"):
                        description = ET.SubElement(contentit, "Description")
                        description.text = file.get("IPTC:Caption-Abstract")
                    else:
                        pass

                # Ajout d'éléments Tag si des mots-clés sont présents dans les métadonnées internes du fichier
                if contentit.find("Tag") is None:
                    # Chercher en priorité les mots-clés issus du champs XMP Subject
                    if file.get("XMP:Subject"):
                        # S'il n'y a qu'un seul mot-clé, créer un élément Tag
                        if not isinstance(file.get("XMP:Subject"), list):
                            tagit = ET.SubElement(contentit, "Tag")
                            tagit.text = str(file.get("XMP:Subject"))
                        else:
                            # S'il y a une liste de mots-clés, créer un élément par mot-clé de la liste
                            for tag in file.get("XMP:Subject"):
                                tagit = ET.SubElement(contentit, "Tag")
                                tagit.text = str(tag)
                    else:
                        # Si le champs XMP Subject est vide, chercher des mots-clés dans le champ IPTC Keywords
                        if file.get("IPTC:Keywords"):
                            # S'il n'y a qu'un seul mot-clé, créer un élément Tag
                            if not isinstance(file.get("IPTC:Keywords"), list):
                                tagit = ET.SubElement(contentit, "Tag")
                                tagit.text = str(file.get("IPTC:Keywords"))
                            else:
                                # S'il y a une liste de mots-clés, créer un élément par mot-clé de la liste
                                for tag in file.get("IPTC:Keywords"):
                                    tagit = ET.SubElement(contentit, "Tag")
                                    tagit.text = str(tag)
                        else:
                            pass

                # Ajout d'éléments Coverage si des informations de localisation sont présentes
                if contentit.find("Coverage") is None:
                    # Chercher si des champs de localisation sont renseignés dans les métadonnées internes du fichier
                    if file.get("XMP:Country" or "IPTC:Country-PrimaryLocationName" or "XMP:City" or "IPTC:City"):
                        # Créer un élément Coverage
                        cov = ET.SubElement(contentit, "Coverage")
                        # Chercher en priorité des informations de localisation sur le pays dans le champ XMP Country
                        if file.get("XMP:Country"):
                            # Créer l'élément Spatial ayant pour valeur la métadonnée de lieu du pays
                            spatial_pays = ET.SubElement(cov, "Spatial")
                            spatial_pays.text = file.get("XMP:Country")
                        else:
                            # Si le champ XMP Country est vide, chercher le pays dans le champ IPTC équivalent
                            if file.get("IPTC:Country-PrimaryLocationName"):
                                # Créer l'élément Spatial ayant pour valeur la métadonnée de lieu du pays
                                spatial_pays = ET.SubElement(cov, "Spatial")
                                spatial_pays.text = file.get("IPTC:Country-PrimaryLocationName")
                            else:
                                pass
                        # Chercher en priorité des informations de localisation sur la ville dans le champ XMP City
                        if file.get("XMP:City"):
                            # Créer l'élément Spatial ayant pour valeur la métadonnée de lieu de la ville
                            spatial_ville = ET.SubElement(cov, "Spatial")
                            spatial_ville.text = file.get("XMP:City")
                        else:
                            # Si le champ XMP City est vide, chercher le pays dans le champ IPTC City
                            if file.get("IPTC:City"):
                                # Créer l'élément Spatial ayant pour valeur la métadonnée de lieu de la ville
                                spatial_ville = ET.SubElement(cov, "Spatial")
                                spatial_ville.text = file.get("IPTC:City")
                            else:
                                pass
                    else:
                        pass

                # Créer un élément OriginatingAgency contenant l'identifiant du service producteur
                if contentit.find("OriginatingAgency") is None:
                    originating_agency = ET.SubElement(contentit, "OriginatingAgency")
                    ET.SubElement(originating_agency, "Identifier").text = "FRAN_NP_009886"

                # Créer un élément SubmissionAgency contenant l'identifiant du service versant
                if contentit.find("SubmissionAgency") is None:
                    submission_agency = ET.SubElement(contentit, "SubmissionAgency")
                    ET.SubElement(submission_agency, "Identifier").text = "FRAN_NP_009886"

                # Ajout d'éléments AuthorizedAgent si le nom du photographe est présent dans les métadonnées du fichier
                if contentit.find("AuthorizedAgent") is None:
                    # Chercher en priorité le nom du photographe dans le champ IPTC By-line
                    if file.get("IPTC:By-line"):
                        authorized_agent = ET.SubElement(contentit, "AuthorizedAgent")
                        # Créer l'élément FullName contenant le nom du photographe issu du champ IPTC By-line
                        fullname = ET.SubElement(authorized_agent, "FullName")
                        fullname.text = file.get("IPTC:By-line")
                        # Créer les éléments Activity et Mandate avec leurs valeurs respectives
                        ET.SubElement(authorized_agent, "Activity").text = "Photographe"
                        ET.SubElement(authorized_agent, "Mandate").text = "Photographe Présidence"
                    else:
                        # Si le champ IPTC By-line est vide, chercher le pays dans le champ EXIF Artist
                        if file.get("EXIF:Artist"):
                            authorized_agent = ET.SubElement(contentit, "AuthorizedAgent")
                            # Créer l'élément FullName contenant le nom du photographe issu du champ EXIF Artist
                            fullname = ET.SubElement(authorized_agent, "FullName")
                            fullname.text = file.get("EXIF:Artist")
                            # Créer les éléments Activity et Mandate avec leurs valeurs respectives
                            ET.SubElement(authorized_agent, "Activity").text = "Photographe"
                            ET.SubElement(authorized_agent, "Mandate").text = "Photographe Présidence"
                        else:
                            pass

                # Ajout d'éléments StartDate et EndDate si des métadonnées de date sont présentes dans le fichier
                if contentit.find("StartDate") is None:
                    # Chercher en priorité la date dans le champ XMP CreateDate
                    if file.get("XMP:CreateDate"):
                        createdate = file.get("XMP:CreateDate")
                        # Si la date ne comporte pas de champ "secondes", en créer un avec une valeur fixe de "00"
                        if len(createdate) == 16:
                            createdate += ":00"
                        else:
                            createdate = createdate
                        # Expression régulière pour isoler les éléments de date qu'on souhaite récupérer
                        match = re.match(r"(\d{4}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2})(\.\d+)?([-+]\d{2}:\d{2})?",
                                         createdate)
                        if match:
                            # Match sur le groupe 1 de l'expression régulière
                            createdate = match.group(1)
                            # Définition du format de date actuel
                            createdate = datetime.strptime(createdate, "%Y:%m:%d %H:%M:%S")
                            # Transformation vers le format de date souhaité
                            createdate = createdate.strftime("%Y-%m-%dT%H:%M:%S")
                            # Création des éléments StartDate et EndDate avec pour valeur la date modifiée
                            startdateit = ET.SubElement(contentit, "StartDate")
                            startdateit.text = createdate
                            enddateit = ET.SubElement(contentit, "EndDate")
                            enddateit.text = createdate
                        else:
                            pass
                    else:
                        # Si le champ XMP CreateDate est vide, chercher la date dans le champ EXIF CreateDate
                        if file.get("EXIF:CreateDate"):
                            createdate = file.get("EXIF:CreateDate")
                            # Si la date ne comporte pas de champ "secondes", en créer un avec une valeur fixe de "00"
                            if len(createdate) == 16:
                                createdate += ":00"
                            else:
                                createdate = createdate
                            # Expression régulière pour isoler les éléments de date qu'on souhaite récupérer
                            match = re.match(r"(\d{4}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2})(\.\d+)?([-+]\d{2}:\d{2})?",
                                             createdate)
                            if match:
                                # Match sur le groupe 1 de l'expression régulière
                                createdate = match.group(1)
                                # Définition du format de date actuel
                                createdate = datetime.strptime(createdate, "%Y:%m:%d %H:%M:%S")
                                # Transformation vers le format de date souhaité
                                createdate = createdate.strftime("%Y-%m-%dT%H:%M:%S")
                                # Création des éléments StartDate et EndDate avec pour valeur la date modifiée
                                startdateit = ET.SubElement(contentit, "StartDate")
                                startdateit.text = createdate
                                enddateit = ET.SubElement(contentit, "EndDate")
                                enddateit.text = createdate
                            else:
                                pass
                        else:
                            pass

    # Création de l'élément DataObjectReference (complété plus tard)
    data_object_reference = ET.SubElement(arch_unit_item, "DataObjectReference")
    ET.SubElement(data_object_reference, "DataObjectGroupReferenceId")

    return arch_unit_item  # Retourner l'élément ArchiveUnit créé


def delete_duplicate_dog(arbre):
    """
    Supprime les groupes DataObjectGroup qui sont des doublons techniques d'autres DataObjectGroup.

    :param xml.etree.ElementTree.Element arbre: L'arbre xml à mettre à jour.

    :return: xml.etree.ElementTree.Element - L'arbre XML modifié avec les doublons supprimés.
    """
    # Dictionnaire pour stocker les objets uniques par leur empreinte et nom de fichier
    objets_uniques = {}
    # Liste pour stocker les objets à supprimer
    objects_a_supprimer = []

    # Trouve l'élément DataObjectPackage dans l'arbre
    data_object_package = arbre.find(".//DataObjectPackage")

    # Parcourt tous les DataObjectGroup dans le DataObjectPackage
    for data_object_group in data_object_package.findall("DataObjectGroup"):
        # Trouve l'élément BinaryDataObject dans le DataObjectGroup
        binary_data_object = data_object_group.find("BinaryDataObject")
        # Extrait le texte de l'élément MessageDigest
        message_digest = binary_data_object.find("MessageDigest").text

        objet = message_digest

        # Vérifie si cet objet est déjà dans objets_uniques
        if objet in objets_uniques:
            # Si oui, ajoute le DataObjectGroup actuel à la liste des objets à supprimer
            objects_a_supprimer.append((data_object_group, data_object_package))
        else:
            # Sinon, ajoute cet objet au dictionnaire des objets uniques
            objets_uniques[objet] = data_object_group

    # Supprime tous les DataObjectGroup marqués comme doublons
    for element, parent in objects_a_supprimer:
        parent.remove(element)

    return arbre  # Retourner l'arbre modifié


def id_attrib(arbre, archive_unit_id):
    """
    Ajoute les attributs 'id' et met à jour les références entre les ArchiveUnits et les DataObjectGroup.

    :param xml.etree.ElementTree.Element arbre: L'arbre XML à mettre à jour.
    :param str archive_unit_id: Le numéro d'entrée du SIP, utilisé pour la génération des identifiants.

    :return: xml.etree.ElementTree.Element - L'arbre XML avec les identifiants et les références mis à jour.
    """
    # Racine de l'arbre XML
    root = arbre
    # Trouve l'élément DataObjectPackage dans l'arbre
    data_object_package = root.find("DataObjectPackage")
    # Trouve tous les éléments DataObjectGroup dans DataObjectPackage
    data_object_group = data_object_package.findall(".//DataObjectGroup")
    # Trouve l'élément DescriptiveMetadata dans DataObjectPackage
    descriptive_metadata = data_object_package.find("DescriptiveMetadata")
    # Trouve tous les éléments ArchiveUnit dans DescriptiveMetadata
    aus = descriptive_metadata.findall(".//ArchiveUnit")

    # Initialisation du compteur d'identifiants pour ArchiveUnit
    id_au = 0

    # Parcourt tous les ArchiveUnits trouvés
    for au in aus:
        # Incrémente le compteur d'identifiants
        id_au = id_au+1

        # Assigne un attribut 'id' unique à chaque ArchiveUnit
        au.set("id", "AU"+str(id_au))

        # Trouve les éléments DataObjectGroupReferenceId et ArchivalAgencyArchiveUnitIdentifier dans ArchiveUnit
        data_object_group_ref_id = au.find(".//DataObjectGroupReferenceId")
        archival_agency_archive_unit_identifier = au.find(".//ArchivalAgencyArchiveUnitIdentifier")

        # Met à jour le texte de l'élément ArchivalAgencyArchiveUnitIdentifier
        archival_agency_archive_unit_identifier.text = archive_unit_id+str(id_au)

        # Vérifie si le niveau de description est 'Item' pour n'itérer que sur les UA de fichiers
        if au.find(".//DescriptionLevel").text == "Item":
            # Trouve le hash temporaire dans BaliseTemp
            temp_hash = au.find(".//BaliseTemp").text
            got = 0

            # Parcourt tous les DataObjectGroup
            for obj in data_object_group:
                got = got + 1
                # Assigne des attributs 'id' uniques à chaque DataObjectGroup et son BinaryDataObject
                obj.set('id', 'GOT' + str(got))
                binary_data_object = obj.find("BinaryDataObject")
                binary_data_object.set('id', 'BDO'+str(got))

                # Met à jour l'URI dans BinaryDataObject
                myid = binary_data_object.attrib['id']
                uri = binary_data_object.find("Uri")
                filename = obj.find(".//Filename").text
                uri.text = 'content/' + myid + "." + filename.split('.')[-1]

                # Vérifie si le MessageDigest correspond au hash temporaire
                message_digest = obj.find(".//MessageDigest").text
                obj_id = obj.attrib['id']
                if temp_hash == message_digest:
                    # Met à jour DataObjectGroupReferenceId avec l'identifiant du DataObjectGroup correspondant
                    data_object_group_ref_id.text = obj_id

    return root  # Retourner l'arbre modifié


def create_management_metadata(arbre):
    """
    Crée et ajoute les métadonnées de gestion relatives au SIP.

    :param xml.etree.ElementTree.Element arbre: L'arbre XML à mettre à jour.

    :return: ElementTree Element - L'arbre XML avec les métadonnées descriptives ajoutées ou mises à jour.
    """
    # Racine de l'arbre XML
    root = arbre

    # Trouve l'élément DataObjectPackage dans l'arbre
    data_object_package = root.find("DataObjectPackage")

    # Crée un nouvel élément ManagementMetadata sous DataObjectPackage
    management_metadata = ET.SubElement(data_object_package, "ManagementMetadata")

    # Ajoute les attributs XMLNS à ManagementMetadata
    management_metadata.set('xmlns', 'fr:gouv:culture:archivesdefrance:seda:v2.1')
    management_metadata.set('xmlns:ns2', 'http://www.w3.org/1999/xlink')

    # Ajoute des sous-éléments avec des valeurs de texte prédéfinies
    ET.SubElement(management_metadata, "ArchivalProfile").text = "FRAN_PR_0001"
    ET.SubElement(management_metadata, "AcquisitionInformation").text = "Versement"
    ET.SubElement(management_metadata, "LegalStatus").text = "Public Archive"
    ET.SubElement(management_metadata, "OriginatingAgencyIdentifier").text = "FRAN_NP_009886"
    ET.SubElement(management_metadata, "SubmissionAgencyIdentifier").text = "FRAN_NP_009886"

    # Trouve l'élément DescriptiveMetadata dans DataObjectPackage
    descriptive_metadata = data_object_package.find("DescriptiveMetadata")

    # Trouve tous les éléments ArchiveUnit dans DescriptiveMetadata
    aus = descriptive_metadata.findall(".//ArchiveUnit")

    # Parcourt tous les ArchiveUnits trouvés
    for au in aus:
        # Trouve l'élément Content dans chaque ArchiveUnit
        content = au.find("Content")

        # Si l'élément BaliseTemp existe dans Content, le supprime
        if content.find("BaliseTemp") is not None:
            temp_hash = content.find("BaliseTemp")
            content.remove(temp_hash)
        else:
            pass
    return root  # Retourner l'arbre modifié


def copy(target_dir, arbre, data):
    """
    Copie les fichiers correspondant aux objets du paquet d'archives vers un répertoire cible, en utilisant
    les données de hachage SHA-512 pour identifier les fichiers correspondants.

    :param str target_dir: Le répertoire cible où les fichiers doivent être copiés.
    :param xml.etree.ElementTree.Element arbre: L'élément racine de l'arbre XML représentant le paquet d'archives.
    :param list[dict] data: une liste de dictionnaires contenant les métadonnées des fichiers (fusion des exports
    Siegfried et Exiftool).

    :return: None.
    """
    # Racine de l'arbre XML
    root = arbre

    # Trouve l'élément DataObjectPackage dans l'arbre
    data_object_package = root.find("DataObjectPackage")

    # Trouve tous les éléments DataObjectGroup dans DataObjectPackage
    data_object_group = data_object_package.findall("DataObjectGroup")

    # Parcourt chaque DataObjectGroup
    for objet in data_object_group:
        # Récupère le nom de fichier
        file_name = objet.find(".//Filename").text

        # Trouve l'élément BinaryDataObject et son message digest
        binary_data_object = objet.find("BinaryDataObject")
        message_digest = binary_data_object.find("MessageDigest").text

        # Crée un nouveau nom de fichier en utilisant l'attribut 'id' et l'extension du fichier original
        new_name = binary_data_object.attrib['id']
        oldext = os.path.splitext(file_name)[1]
        new_name = new_name + oldext

        # Crée le chemin complet vers le nouveau fichier dans le répertoire cible
        new_path = os.path.join(target_dir, new_name)

        # Parcourt les données de métadonnées pour trouver le fichier correspondant au message digest
        for item in data:
            files = item.get("files", [])
            for file in files:
                # Vérifier que les empreintes matchent
                if message_digest == file.get("sha512"):
                    # Récupère l'ancien chemin du fichier et copie le fichier vers le nouveau chemin
                    old_path = file.get("filename")
                    shutil.copy(old_path, new_path)


def main():

    input("Bienvenue dans la moulinette de fabrication de SIP pour les reportages photographiques de la Présidence de "
          "la République. Appuyez sur Entrée pour commencer.")

    archive_unit_id = get_archiveunit_id()
    print(archive_unit_id)

    rattachement = updateoperation()

    value = comment_message_id()

    selected_directory = select_directory()
    print("Dossier sélectionné :", selected_directory)

    data_ir = select_csv()
    print("Fichier de métadonnées externe sélectionné.")

    liste_rp = select_list_rp()
    print("Reportages sélectionnés :", liste_rp)

    target_dir = chose_target_dir()
    print("Répertoire cible :", target_dir)

    print("Extraction des métadonnées internes des photos.")
    data_exif = exif_extract(selected_directory, liste_rp)
    data_sig = siegfried(selected_directory, liste_rp)
    data = metadata_json(data_sig, data_exif)

    print("Création de l'en-tête du manifest.")
    root = creer_root(value)
    print("Création des DataObjectGroup.")
    root = create_dataobjectgroup(root, selected_directory, liste_rp)
    print("Ajout des métadonnées aux DataObjectGroup")
    root = package_metadata(root, data)
    print("Création des éléments ArchiveUnit.")
    arbre = ua_rp(selected_directory, data_ir, root, data, liste_rp, rattachement)
    print("Suppression des doublons dans les DataObjectGroup.")
    arbre = delete_duplicate_dog(arbre)
    print("Attribution des identifiants.")
    arbre = id_attrib(arbre, archive_unit_id)
    print("Création de l'élément DescriptiveMetadata.")
    arbre = create_management_metadata(arbre)
    print("Ecriture du manifest.")
    arbre_str = minidom.parseString(ET.tostring(arbre, encoding='unicode')).toprettyxml(indent="   ")
    target_manifest = os.path.split(target_dir)
    target_manifest = target_manifest[0]
    target_manifest = os.path.join(target_manifest, "manifest.xml")
    with open(target_manifest, "w", encoding="utf-8") as f:
        f.write(arbre_str)

    print("Copie et renommage des fichiers dans le dossier content.")
    copy(target_dir, arbre, data)
    print("Bravo, le paquet est terminé !")
    input("Appuyez sur Entrée pour fermer l'application.")


if __name__ == "__main__":
    main()
