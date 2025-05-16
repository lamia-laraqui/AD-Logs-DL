
Vous etes maintenant dans etape 1 pour executer ce projet.


# /!\ : PENSEZ A LIRE README.md DU DOSSIER DataSet_HDFS avant de commencer a executer

# ETAPE 1 : Extraction et Préparation des Logs

### Objectif de l'Étape
La première étape du projet consiste à transformer les données de logs bruts en un format structuré. Cette transformation est essentielle pour la suite des analyses et permettra de créer un modèle d'identification d'anomalies basé sur les modèles d'événements présents dans les logs. Le processus de parsing utilise l’algorithme Drain, qui est optimisé pour analyser les logs de manière hiérarchique, facilitant ainsi la détection de motifs répétitifs et la craétion de "templates" (modèles d’événements).

## Structure et Contenu du Répertoire parse

1. Fichiers et Scripts

- raw_data.ipynb : un notebook Jupyter pour explorer les données et effectuer des transformations initiales. ['Premier code qui doit etre executer dans cette etape en general']
- project_parser.py : le script principal de parsing. Il lit les fichiers de logs bruts et génère des fichiers structurés. ['deuxieme code qui doit etre executer dans cette etape']

2. Dossiers

- DataSet_HDFS : contient les fichiers de logs bruts et les resultats des logs apres parsing.

3. Données Utilisées

Les logs sont issus de la collection HDFS [SOURCE DES DONNEES : https://github.com/logpai/loghub/tree/master]

