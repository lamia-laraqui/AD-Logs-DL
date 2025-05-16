"""
Charge les données semi-structurées de Drain et les transforme pour le CNN.
"""

import numpy as np
import pandas as pd
import time
import os
from Transf_sequ_image import collect_event_ids, FeatureExtractor

if __name__ == "__main__":

    data_version = "_v5"
    data_version = "_tf-idf{}".format(data_version)

    # Emplacements des données
    load_data_location = "C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/parse/DataSet_HDFS/"
    save_location = "C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/process/Datasets/_tf-idf_v5/"

    # Création du dossier de sauvegarde s'il n'existe pas
    os.makedirs(save_location, exist_ok=True)

    start = time.time()

    # Chargement des données
    print("loading x_train")
    x_train = pd.read_csv("{}HDFS_train.log_structured.csv".format(load_data_location))

    print("loading x_test")
    x_test = pd.read_csv("{}HDFS_test.log_structured.csv".format(load_data_location))

    print("loading y")
    y = pd.read_csv("{}anomaly_label.csv".format(load_data_location))

    # Traitement des événements en blocs
    re_pat = r"(blk_-?\d+)"
    col_names = ["BlockId", "EventSequence"]

    print("collecting events for x_train")
    events_train = collect_event_ids(x_train, re_pat, col_names)
    print("collecting events for x_test")
    events_test = collect_event_ids(x_test, re_pat, col_names)

    print("merging block frames with labels")
    events_train = events_train.merge(y, on="BlockId")
    events_test = events_test.merge(y, on="BlockId")

    print("removing blocks that are overlapped into train and test")
    overlapping_blocks = np.intersect1d(events_train["BlockId"], events_test["BlockId"])
    events_train = events_train[~events_train["BlockId"].isin(overlapping_blocks)]
    events_test = events_test[~events_test["BlockId"].isin(overlapping_blocks)]

    events_train_values = events_train["EventSequence"].values
    events_test_values = events_test["EventSequence"].values

    # Vérification de la longueur minimale des séquences pour ajuster la taille de la fenêtre
    sequence_lengths = [len(seq) for seq in events_train_values]
    print("Longueur minimale des séquences :", min(sequence_lengths))
    print("Longueur moyenne des séquences :", sum(sequence_lengths) / len(sequence_lengths))

    # Ajustement de la taille de la fenêtre en fonction de la longueur minimale
    window_size = min(10, min(sequence_lengths)) 

    # Initialisation de l'extracteur de caractéristiques
    fe = FeatureExtractor()

    print("fit_transform x_train")
    subblocks_train = fe.fit_transform(
        events_train_values,
        term_weighting="tf-idf",
        length_percentile=95,
        window_size=window_size,
    )

    print("transform x_test")
    subblocks_test = fe.transform(events_test_values)

    print("collecting y data")
    y_train = events_train[["BlockId", "Label"]]
    y_test = events_test[["BlockId", "Label"]]

    # Sauvegarde des fichiers de sortie
    print("writing y to csv")
    y_train.to_csv("{}y_train{}.csv".format(save_location, data_version), index=False)
    y_test.to_csv("{}y_test{}.csv".format(save_location, data_version), index=False)

    print("saving x to numpy object")
    np.save("{}x_train{}.npy".format(save_location, data_version), subblocks_train)
    np.save("{}x_test{}.npy".format(save_location, data_version), subblocks_test)

    print("time taken :", time.time() - start)
