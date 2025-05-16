"""
ETAPE 1 :
L'objectif principal de project_parser.py est de transformer des logs bruts en un format structuré où chaque message est associé à un modèle (template). Cette structuration simplifie les étapes suivantes d'extraction de caractéristiques et d'entraînement du modèle.

NP : avant d'executer le code suivant, il faut premierement generer le fichier HDFS_2k_train.log a partir du code raw_data.ipynb
"""

from logparser import Drain

"""
Drain est une technique de parsing de logs qui utilise des arbres pour identifier des modèles répétitifs dans les logs et créer des "templates" (modèles) d'événements.

input_dir : Répertoire où se trouvent les logs bruts non structurés.

output_dir : Répertoire où les résultats du parsing seront stockés.

log_file_all et log_file_train : Noms des fichiers de logs. HDFS.log est le log complet, tandis que HDFS_train.log est un sous-ensemble utilisé pour l'entraînement.

log_format : Le format des logs est défini pour aider Drain à reconnaître les éléments dans chaque ligne du log.
"""

input_dir = "C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/parse/DataSet_HDFS/"
output_dir = "C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/parse/DataSet_HDFS/"  
log_file_all = "HDFS.log" 
log_file_train = "HDFS_train.log"  
log_format = "<Date> <Time> <Pid> <Level> <Component>: <Content>" 
# Expressions Régulières pour le Prétraitement
regex = [
    r"blk_(|-)[0-9]+",  # ID de bloc
    r"(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)",  # Adresse IP
    r"(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$",  # Nombres
]

"""
ID de bloc (blk_(|-)[0-9]+) : Supprime ou anonymise les identifiants de bloc.

Adresse IP ((/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)) : Supprime ou masque les adresses IP.

Nombres ((?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$) : Supprime ou masque les valeurs numériques.
"""

st = 0.5  # Seuil de similarité
depth = 4  # Profondeur des nœuds feuilles

"""
st (similarity threshold) : Définit le seuil de similarité pour regrouper les messages similaires sous un même modèle. Un seuil de 0,5 signifie que les messages doivent être au moins similaires à 50 % pour être regroupés ensemble.
depth : Détermine la profondeur maximale des nœuds dans l’arbre de parsing. Une profondeur de 4 permet à Drain de capturer des motifs plus complexes sans générer un arbre trop profond.
"""

# I. Parsing des Fichiers de Log

# I.1. run on training dataset.
# parser = Drain.LogParser(
#     log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex
# )
# parser.parse(log_file_all)

# I.2.run on complete dataset
parser = Drain.LogParser(
    log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex
)
parser.parse(log_file_train)

"""
Ces lignes définissent et exécutent le parseur de logs Drain.
Création d'un Objet LogParser : Drain.LogParser est initialisé avec les paramètres de format du log, le répertoire d’entrée, le répertoire de sortie, la profondeur de l’arbre, le seuil de similarité et les expressions régulières.
Parsing des Logs :
    - parser.parse(log_file_all) lance le parsing du fichier complet HDFS.log.
    - parser.parse(log_file_train) lance le parsing du fichier de logs pour l’entraînement HDFS_train.log.
"""