


# ETAPE 2 : Extraction des Caractéristiques et Préparation des Données pour le Modèle CNN

## Objectif de l'Étape

Cette étape consiste à transformer les logs structurés en matrices de caractéristiques utilisables pour un modèle de détection d'anomalies basé sur un réseau de neurones convolutif (CNN). 

Le but est de créer des représentations visuelles des logs sous forme d'images temporelles, permettant au modèle CNN d'apprendre des motifs et de détecter les anomalies. Cette transformation repose sur des techniques de fenêtrage glissant et de pondération TF-IDF pour capturer les séquences d'événements dans les logs.

## Structure et Contenu du Répertoire process

1. Scripts et Notebooks

- Transf_sequ_image.py : un module de traitement dédié pour transformer les séquences d'événements en images temporelles exploitables par le CNN. [Le premier fichier a executé dans cette étape]
- project_processor.py : le script principal qui charge les données de logs structurés, applique les transformations, et sauvegarde les matrices de caractéristiques. [Le deuxieme fichier a executé dans cette étape]

2. Données Utilisées 

- Les logs structurés générés lors de l'Étape 1 sont chargés pour appliquer des transformations avancées, avec notamment la création de sous-blocs d'événements pondérés par TF-IDF, et la génération d'images temporelles par fenêtrage glissant.

3. Instructions d'Exécution

- Assurer la Disponibilité des Fichiers Structurés.
- Assurez-vous que les fichiers structurés sont présents dans le dossier parser/DataSet_HDFS et qu'ils ont été générés lors de l'Étape 1. Ces fichiers incluent :

HDFS_train.log_structured.csv : logs structurés pour l’entraînement.
HDFS_test.log_structured.csv : logs structurés pour le test.

Après l'exécution, les fichiers de caractéristiques sont sauvegardés dans le dossier Datasets avec le suffixe _tf-idf_v5. Ces fichiers seront utilisés pour entraîner le modèle CNN dans l’étape suivante.

En suivant ces étapes, vous pouvez préparer les données pour la détection d'anomalies avec un modèle CNN basé sur les motifs d'événements identifiés dans les logs.

