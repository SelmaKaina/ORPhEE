import os
import shutil


def copy_rename(target_dir, arbre, data):
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