from . import import_data, manifest_creation, copy_files

from datetime import datetime
import logging
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QCheckBox, QFileDialog,
    QHBoxLayout, QGridLayout, QScrollArea, QComboBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -*- coding: utf-8 -*-

# Import de la date du jour de fabrication du SIP
date_ajd = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ORPhEE")
        # Style pour l'ensemble de l'application
        self.setStyleSheet("""
            background-color: #f6ecdb;
            font-size: 12px;
            font-family: Cambria;
            padding: 10px;
        """)
        self.resize(800, 600)
        self.setWindowIcon(QIcon("./package/lyre.png"))

        # Texte introductif
        intro_label = QLabel("Veuillez remplir le formulaire ci-dessous :")
        intro_label.setStyleSheet("color: #865746;")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Créer les widgets pour les champs de texte existants
        self.num_entree = QLabel("Numéro de l'entrée :")
        self.num_entree.setStyleSheet("color: #865746;")
        self.entree_input = QLineEdit()
        self.entree_input.setPlaceholderText("ex : 20240001")

        self.num_paquet = QLabel("Numéro du paquet :")
        self.num_paquet.setStyleSheet("color: #865746;")
        self.paquet_input = QLineEdit()
        self.paquet_input.setPlaceholderText("ex : 1")

        self.versement_label = QLabel("Intitulé du versement :")
        self.versement_label.setStyleSheet("color: #865746;")
        self.versement_input = QLineEdit()
        self.versement_input.setPlaceholderText("Valeur des éléments Comment et MessageIdentifier.")

        # Ajouter les nouveaux champs requis

        self.archival_agency_identifier_label = QLabel("ArchivalAgency Identifier :")
        self.archival_agency_identifier_label.setStyleSheet("color: #865746;")
        self.archival_agency_identifier_input = QLineEdit()
        self.archival_agency_identifier_input.setPlaceholderText("Identifiant du service d'archives.")

        self.transferring_agency_identifier_label = QLabel("TransferringAgency :")
        self.transferring_agency_identifier_label.setStyleSheet("color: #865746;")
        self.transferring_agency_identifier_input = QLineEdit()
        self.transferring_agency_identifier_input.setPlaceholderText("Nom du service versant.")

        self.originating_agency_identifier_label = QLabel("OriginatingAgency Identifier :")
        self.originating_agency_identifier_label.setStyleSheet("color: #865746;")
        self.originating_agency_identifier_input = QLineEdit()
        self.originating_agency_identifier_input.setPlaceholderText("Identifiant du service producteur.")

        self.submission_agency_identifier_label = QLabel("SubmissionAgency :")
        self.submission_agency_identifier_label.setStyleSheet("color: #865746;")
        self.submission_agency_identifier_input = QLineEdit()
        self.submission_agency_identifier_input.setPlaceholderText("Identifiant du service versant responsable du transfert de données.")


        self.archival_agreement_label = QLabel("ArchivalAgreement :")
        self.archival_agreement_label.setStyleSheet("color: #865746;")
        self.archival_agreement_input = QLineEdit()
        self.archival_agreement_input.setPlaceholderText("Référence à un accord de service / contrat d'entrée.")

        self.authorized_agent_activity_label = QLabel("AuthorizedAgent Activity :")
        self.authorized_agent_activity_label.setStyleSheet("color: #865746;")
        self.authorized_agent_activity_input = QLineEdit()
        self.authorized_agent_activity_input.setPlaceholderText("Activité de la personne détenant des droits sur la photo (ex : Photographe).")

        self.authorized_agent_mandate_label = QLabel("AuthorizedAgent Mandate :")
        self.authorized_agent_mandate_label.setStyleSheet("color: #865746;")
        self.authorized_agent_mandate_input = QLineEdit()
        self.authorized_agent_mandate_input.setPlaceholderText("Statut du détenteur de droits (ex : Photographe service public, d'agence, privé).")

        self.archival_profile_label = QLabel("ArchivalProfile :")
        self.archival_profile_label.setStyleSheet("color: #865746;")
        self.archival_profile_input = QLineEdit()
        self.archival_profile_input.setPlaceholderText("Référence au profil d’archivage applicable aux unités d’archives.")

        self.acquisition_information_label = QLabel("AcquisitionInformation :")
        self.acquisition_information_label.setStyleSheet("color: #865746;")
        self.acquisition_information_input = QLineEdit()
        self.acquisition_information_input.setPlaceholderText("Référence aux modalités d'entrée des archives.")


        self.legal_status_label = QLabel("LegalStatus :")
        self.legal_status_label.setStyleSheet("color: #865746;")
        self.legal_status_input = QComboBox()
        self.legal_status_input.addItems(["Public Archive", "Private Archive", "Public and Private Archive"])

        # Cases à cocher pour les valeurs à sélectionner
        self.metadata_checkboxes = []
        createdate = QCheckBox(f"-CreateDate")
        createdate.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(createdate)

        modifdate = QCheckBox(f"-FileModifyDate")
        modifdate.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(modifdate)

        by_line = QCheckBox(f"-By-line")
        by_line.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(by_line)

        artist = QCheckBox(f"-Artist")
        artist.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(artist)

        creator = QCheckBox(f"-Creator")
        creator.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(creator)

        city = QCheckBox(f"-City")
        city.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(city)

        country = QCheckBox(f"-Country")
        country.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(country)

        country_pln = QCheckBox(f"-Country-PrimaryLocationName")
        country_pln.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(country_pln)

        caption = QCheckBox(f"-Caption-Abstract")
        caption.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(caption)

        description = QCheckBox(f"-Description")
        description.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(description)

        subject = QCheckBox(f"-Subject")
        subject.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(subject)

        keywords = QCheckBox(f"-Keywords")
        keywords.setStyleSheet("color: #865746;")
        self.metadata_checkboxes.append(keywords)

        # Créer la checkbox pour les champs optionnels
        self.optional_checkbox = QCheckBox("Effectuer un rattachement à une autre unité archivistique")
        self.optional_checkbox.setStyleSheet("color: #865746;")
        self.optional_checkbox.stateChanged.connect(self.toggle_optional_fields)

        # Créer les widgets pour les champs de texte optionnels
        self.rattachement_label = QLabel("Cote de l'UA de rattachement :")
        self.rattachement_label.setStyleSheet("color: #865746;")
        self.rattachement_input = QLineEdit()

        self.nom_rattachement_label = QLabel("Nom de l'UA de rattachement :")
        self.nom_rattachement_label.setStyleSheet("color: #865746;")
        self.nom_rattachement_input = QLineEdit()

        # Initialement, les champs optionnels ne sont pas visibles
        self.rattachement_label.setVisible(False)
        self.rattachement_input.setVisible(False)
        self.nom_rattachement_label.setVisible(False)
        self.nom_rattachement_input.setVisible(False)

        # Boutons pour sélectionner répertoires et fichiers
        self.entree_dir_button = QPushButton("Sélectionner le répertoire contenant les reportages")
        self.entree_dir_button.setStyleSheet("background-color: #1c85f6; color: #fffbef;")
        self.entree_dir_button.clicked.connect(self.select_entree_dir)
        self.entree_dir_label = QLabel("Aucun répertoire sélectionné")
        self.entree_dir_label.setStyleSheet("color: #865746;")

        self.cible_dir_button = QPushButton("Sélectionner le répertoire où sera créé le SIP")
        self.cible_dir_button.setStyleSheet("background-color: #1c85f6; color: #fffbef;")
        self.cible_dir_button.clicked.connect(self.select_cible_dir)
        self.cible_dir_label = QLabel("Aucun répertoire sélectionné")
        self.cible_dir_label.setStyleSheet("color: #865746;")

        self.csv_file_button = QPushButton("Sélectionner l'instrument de recherche (CSV)")
        self.csv_file_button.setStyleSheet("background-color: #1c85f6; color: #fffbef;")
        self.csv_file_button.clicked.connect(self.select_csv_file)
        self.csv_file_label = QLabel("Aucun fichier CSV sélectionné")
        self.csv_file_label.setStyleSheet("color: #865746;")

        self.txt_file_button = QPushButton("Sélectionner la liste des reportages (TXT)")
        self.txt_file_button.setStyleSheet("background-color: #1c85f6; color: #fffbef;")
        self.txt_file_button.clicked.connect(self.select_txt_file)
        self.txt_file_label = QLabel("Aucun fichier texte sélectionné")
        self.txt_file_label.setStyleSheet("color: #865746;")

        # Créer un bouton de soumission
        self.submit_button = QPushButton("Soumettre")
        self.submit_button.setStyleSheet("background-color: #F5BD02; color: #fffbef;")
        self.submit_button.clicked.connect(self.handle_submit)  # Connecter à la fonction de traitement
        self.submit_button.setEnabled(False)  # Initialement désactivé

        # Créer un layout en grille pour organiser les widgets
        grid_layout = QGridLayout()
        grid_layout.addWidget(intro_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.num_entree, 1, 0)
        grid_layout.addWidget(self.entree_input, 1, 1)
        grid_layout.addWidget(self.num_paquet, 2, 0)
        grid_layout.addWidget(self.paquet_input, 2, 1)
        grid_layout.addWidget(self.versement_label, 3, 0)
        grid_layout.addWidget(self.versement_input, 3, 1)
        grid_layout.addWidget(self.archival_agency_identifier_label, 4, 0)
        grid_layout.addWidget(self.archival_agency_identifier_input, 4, 1)
        grid_layout.addWidget(self.transferring_agency_identifier_label, 5, 0)
        grid_layout.addWidget(self.transferring_agency_identifier_input, 5, 1)
        grid_layout.addWidget(self.originating_agency_identifier_label, 6, 0)
        grid_layout.addWidget(self.originating_agency_identifier_input, 6, 1)
        grid_layout.addWidget(self.submission_agency_identifier_label, 7, 0)
        grid_layout.addWidget(self.submission_agency_identifier_input, 7, 1)
        grid_layout.addWidget(self.archival_agreement_label, 8, 0)
        grid_layout.addWidget(self.archival_agreement_input, 8, 1)
        grid_layout.addWidget(self.authorized_agent_activity_label, 9, 0)
        grid_layout.addWidget(self.authorized_agent_activity_input, 9, 1)
        grid_layout.addWidget(self.authorized_agent_mandate_label, 10, 0)
        grid_layout.addWidget(self.authorized_agent_mandate_input, 10, 1)
        grid_layout.addWidget(self.archival_profile_label, 11, 0)
        grid_layout.addWidget(self.archival_profile_input, 11, 1)
        grid_layout.addWidget(self.acquisition_information_label, 12, 0)
        grid_layout.addWidget(self.acquisition_information_input, 12, 1)
        grid_layout.addWidget(self.legal_status_label, 13, 0)
        grid_layout.addWidget(self.legal_status_input, 13, 1)

        # Ajouter les cases à cocher pour les métadonnées
        metadata_label = QLabel("Métadonnées internes à extraire :")
        metadata_label.setStyleSheet("color: #865746;")
        grid_layout.addWidget(metadata_label, 14, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        row = 17
        col = 0
        # Ajouter les checkboxes dans des QVBoxLayout pour les centrer en colonnes
        checkbox_column1 = QVBoxLayout()
        checkbox_column2 = QVBoxLayout()
        checkbox_column3 = QVBoxLayout()

        for checkbox in self.metadata_checkboxes[:4]:
            checkbox_column1.addWidget(checkbox)
        for checkbox in self.metadata_checkboxes[4:8]:
            checkbox_column2.addWidget(checkbox)
        for checkbox in self.metadata_checkboxes[8:]:
            checkbox_column3.addWidget(checkbox)

        # Ajouter ces QVBoxLayout dans un QHBoxLayout pour centrer les colonnes
        metadata_layout = QHBoxLayout()
        metadata_layout.addLayout(checkbox_column1)
        metadata_layout.addLayout(checkbox_column2)
        metadata_layout.addLayout(checkbox_column3)

        grid_layout.addLayout(metadata_layout, 15, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Ajouter la checkbox optionnelle et les champs optionnels
        grid_layout.addWidget(self.optional_checkbox, row + 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.rattachement_label, row + 2, 0)
        grid_layout.addWidget(self.rattachement_input, row + 2, 1)
        grid_layout.addWidget(self.nom_rattachement_label, row + 3, 0)
        grid_layout.addWidget(self.nom_rattachement_input, row + 3, 1)

        # Ajouter les boutons pour sélectionner les répertoires et fichiers
        grid_layout.addWidget(self.entree_dir_button, row + 4, 0)
        grid_layout.addWidget(self.entree_dir_label, row + 4, 1)
        grid_layout.addWidget(self.cible_dir_button, row + 5, 0)
        grid_layout.addWidget(self.cible_dir_label, row + 5, 1)
        grid_layout.addWidget(self.csv_file_button, row + 6, 0)
        grid_layout.addWidget(self.csv_file_label, row + 6, 1)
        grid_layout.addWidget(self.txt_file_button, row + 7, 0)
        grid_layout.addWidget(self.txt_file_label, row + 7, 1)

        # Ajouter le bouton Soumettre en bas, centré
        grid_layout.addWidget(self.submit_button, row + 8, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Créer un widget pour le contenu principal et définir le layout
        main_widget = QWidget()
        main_widget.setLayout(grid_layout)

        # Créer une zone de défilement pour le widget principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_widget)

        self.setCentralWidget(scroll_area)

        # Connecter la vérification des champs obligatoires
        self.entree_input.textChanged.connect(self.check_fields)
        self.paquet_input.textChanged.connect(self.check_fields)
        self.versement_input.textChanged.connect(self.check_fields)
        self.archival_agency_identifier_input.textChanged.connect(self.check_fields)
        self.transferring_agency_identifier_input.textChanged.connect(self.check_fields)
        self.originating_agency_identifier_input.textChanged.connect(self.check_fields)
        self.submission_agency_identifier_input.textChanged.connect(self.check_fields)
        self.archival_agreement_input.textChanged.connect(self.check_fields)
        self.authorized_agent_activity_input.textChanged.connect(self.check_fields)
        self.authorized_agent_mandate_input.textChanged.connect(self.check_fields)
        self.archival_profile_input.textChanged.connect(self.check_fields)
        self.acquisition_information_input.textChanged.connect(self.check_fields)
        self.legal_status_input.currentTextChanged.connect(self.check_fields)

        # Vérifier les champs au démarrage de l'application
        self.check_fields()

    def check_fields(self):
        # Vérifier si tous les champs obligatoires sont remplis pour activer le bouton Soumettre
        mandatory_fields = [
            self.entree_input, self.paquet_input, self.versement_input,
            self.transferring_agency_identifier_input, self.originating_agency_identifier_input,
            self.submission_agency_identifier_input, self.archival_agreement_input,
            self.authorized_agent_activity_input, self.authorized_agent_mandate_input,
            self.archival_profile_input, self.acquisition_information_input
        ]

        for field in mandatory_fields:
            if field.text().strip() == "":
                self.submit_button.setEnabled(False)
                return

        # Vérifier le champ Legal Status
        if self.legal_status_input.currentText().strip() == "":
            self.submit_button.setEnabled(False)
            return

        self.submit_button.setEnabled(True)

    def toggle_optional_fields(self):
        # Afficher ou cacher les champs optionnels en fonction de l'état de la checkbox
        is_checked = self.optional_checkbox.isChecked()
        self.rattachement_label.setVisible(is_checked)
        self.rattachement_input.setVisible(is_checked)
        self.nom_rattachement_label.setVisible(is_checked)
        self.nom_rattachement_input.setVisible(is_checked)

    def select_entree_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire contenant les reportages")
        if directory:
            self.entree_dir_label.setText(directory)

    def select_cible_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire où sera créé le SIP")
        if directory:
            self.cible_dir_label.setText(directory)

    def select_csv_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Sélectionner l'instrument de recherche (CSV)", "", "CSV Files (*.csv)")
        if file:
            self.csv_file_label.setText(file)

    def select_txt_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Sélectionner la liste des reportages (TXT)", "", "Text Files (*.txt)")
        if file:
            self.txt_file_label.setText(file)

    def submit(self):
        # Récupérer les valeurs des champs de texte
        entree_dir = self.entree_dir_label.text()
        cible_dir = self.cible_dir_label.text()
        csv_file = self.csv_file_label.text()
        txt_file = self.txt_file_label.text()

        # Vérifier si les champs de rattachement sont vides
        rattachement_value = self.rattachement_input.text().strip()
        nom_rattachement_value = self.nom_rattachement_input.text().strip()

        if rattachement_value or nom_rattachement_value:
            rattachement_data = [rattachement_value if rattachement_value else "N/A",
                                 nom_rattachement_value if nom_rattachement_value else "N/A"]
        else:
            rattachement_data = None

        data = {
            "Num_entree": self.entree_input.text(),
            "Num_paquet": self.paquet_input.text(),
            "Versement": self.versement_input.text(),
            "ArchivalAgency_Identifier": self.archival_agency_identifier_input.text(),
            "TransferringAgency_Identifier": self.transferring_agency_identifier_input.text(),
            "OriginatingAgency_Identifier": self.originating_agency_identifier_input.text(),
            "SubmissionAgency_Identifier": self.submission_agency_identifier_input.text(),
            "ArchivalAgreement" : self.archival_agreement_input.text(),
            "AuthorizedAgent_Activity": self.authorized_agent_activity_input.text(),
            "AuthorizedAgent_Mandate": self.authorized_agent_mandate_input.text(),
            "ArchivalProfile": self.archival_profile_input.text(),
            "AcquisitionInformation": self.acquisition_information_input.text(),
            "LegalStatus": self.legal_status_input.currentText(),
            "Champs_metadata": [checkbox.text() for checkbox in self.metadata_checkboxes if checkbox.isChecked()],
            "dir_path": entree_dir,
            "cible": cible_dir,
            "csv": csv_file,
            "liste_rp": txt_file,
            "Rattachement": None
        }

        if rattachement_data is not None:
            data["Rattachement"] = rattachement_data
        else:
            data["Rattachement"] is None

        self.close()


        return data
    def handle_submit(self):
        # Cette fonction est appelée lorsque l'utilisateur clique sur Soumettre
        formulaire = self.submit()

        archival_agency_archive_unit_identifier = formulaire["Num_entree"] + "_" + formulaire["Num_paquet"] + "_"
        archive_unit_id = archival_agency_archive_unit_identifier

        if formulaire["Rattachement"] is not None:
            rattachement = formulaire["Rattachement"]
        else:
            rattachement = None

        value = formulaire["Versement"]

        selected_directory = formulaire["dir_path"]

        csv_file = formulaire["csv"]
        data_ir = import_data.select_csv(csv_file)
        print("Fichier de métadonnées externe sélectionné.")

        liste = formulaire["liste_rp"]
        liste_rp = import_data.select_list_rp(liste)
        print("Reportages sélectionnés :", liste_rp)

        cible_dir = formulaire["cible"]
        target_dir = import_data.chose_target_dir(cible_dir)
        print("Répertoire cible :", target_dir)

        print("Extraction des métadonnées internes des photos.")
        data_exif = import_data.exif_extract(selected_directory, liste_rp, formulaire)
        data_sig = import_data.siegfried(selected_directory, liste_rp)
        data = import_data.metadata_json(data_sig, data_exif)

        print("Création de l'en-tête du manifest.")
        root = manifest_creation.creer_root(value, formulaire)
        print("Création des DataObjectGroup.")
        root = manifest_creation.create_dataobjectgroup(root, selected_directory, liste_rp)
        print("Ajout des métadonnées aux DataObjectGroup")
        root = manifest_creation.package_metadata(root, data)
        print("Création des éléments ArchiveUnit.")
        arbre = manifest_creation.ua_rp(selected_directory, data_ir, root, data, liste_rp, rattachement, formulaire)
        print("Suppression des doublons dans les DataObjectGroup.")
        arbre = manifest_creation.delete_duplicate_dog(arbre)
        print("Attribution des identifiants.")
        arbre = manifest_creation.id_attrib(arbre, archive_unit_id)
        print("Création de l'élément DescriptiveMetadata.")
        arbre = manifest_creation.create_management_metadata(arbre, formulaire)
        print("Ecriture du manifest.")
        manifest_creation.write_xml(arbre, target_dir)

        print("Copie et renommage des fichiers dans le dossier content.")
        copy_files.copy_rename(target_dir, arbre, data)
        print("Bravo, le paquet est terminé !")
        input("Appuyez sur Entrée pour fermer l'application.")
        QApplication.instance().quit()  # Quitter l'application PyQt