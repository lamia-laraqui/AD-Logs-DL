import numpy as np
import pandas as pd
import re
from collections import OrderedDict, Counter
from PIL import Image


def collect_event_ids(data_frame, regex_pattern, column_names):
    """
    Transforme le DataFrame d'entrée en un DataFrame avec deux colonnes :
    BlockId et EventSequence, où EventSequence est une liste des événements 
    survenus pour chaque bloc.
    """
    data_dict = OrderedDict()
    for _, row in data_frame.iterrows():
        blk_id_list = re.findall(regex_pattern, row["Content"])
        blk_id_set = set(blk_id_list)
        for blk_id in blk_id_set:
            if blk_id not in data_dict:
                data_dict[blk_id] = []
            data_dict[blk_id].append(row["EventId"])
    data_df = pd.DataFrame(list(data_dict.items()), columns=column_names)
    return data_df


def windower(sequence, window_size):
    """
    Crée un tableau de fenêtres glissantes. La longueur de sortie est :
    len(sequence) - window_size + 1.
    """
    return np.lib.stride_tricks.sliding_window_view(sequence, window_size)


def sequence_padder(sequence, required_length):
    """
    Remplit la séquence d'événements à droite jusqu'à atteindre la longueur
    maximale spécifiée.
    """
    if len(sequence) > required_length:
        return sequence
    return np.pad(
        sequence,
        (0, required_length - len(sequence)),
        mode="constant",
        constant_values=(0),
    )


def resize_time_image(time_image, size):
    """
    Réduit la taille des images temporelles ayant plus de séquences que 
    la longueur maximale définie.
    """
    width = size[1]
    height = size[0]
    return np.array(Image.fromarray(time_image).resize((width, height)))


class FeatureExtractor(object):
    def __init__(self):
        self.mean_vec = None
        self.idf_vec = None
        self.events = None
        self.term_weighting = None
        self.max_seq_length = None
        self.window_size = None
        self.num_rows = None

    def fit_transform(self, X_seq, term_weighting=None, length_percentile=90, window_size=16):
        """
        Ajuste et transforme l'ensemble d'entraînement.
        X_seq : ndarray, matrice des séquences de logs
        term_weighting : None ou `tf-idf`
        length_percentile : int, définit la longueur max des séquences
        window_size : int, taille de la fenêtre glissante
        """
        self.term_weighting = term_weighting
        self.window_size = window_size

        # Récupère les événements uniques et supprime les doublons
        self.events = list(set(np.concatenate(X_seq).ravel().flatten()))

        # Détermine la longueur max de la séquence en fonction du percentile
        length_list = np.array(list(map(len, X_seq)))
        self.max_seq_length = int(np.percentile(length_list, length_percentile))
        self.num_rows = self.max_seq_length - self.window_size + 1

        print("forme finale sera ", self.num_rows, len(self.events))

        # Crée les images temporelles pour chaque séquence
        time_images = []
        for block in X_seq:
            padded_block = sequence_padder(block, self.max_seq_length)
            time_image = windower(padded_block, self.window_size)
            time_image_counts = []
            for time_row in time_image:
                row_count = Counter(time_row)
                time_image_counts.append(row_count)

            time_image_df = pd.DataFrame(time_image_counts, columns=self.events)
            time_image_df = time_image_df.reindex(sorted(time_image_df.columns), axis=1)
            time_image_df = time_image_df.fillna(0)
            time_image_np = time_image_df.to_numpy()

            if len(time_image_np) > self.num_rows:
                time_image_np = resize_time_image(
                    time_image_np, (self.num_rows, len(self.events)),
                )

            time_images.append(time_image_np)

        X = np.stack(time_images)

        # Applique TF-IDF si spécifié
        if self.term_weighting == "tf-idf":
            dim1, dim2, dim3 = X.shape
            X = X.reshape(-1, dim3)
            df_vec = np.sum(X > 0, axis=0)
            self.idf_vec = np.log(dim1 / (df_vec + 1e-8))
            idf_tile = np.tile(self.idf_vec, (dim1 * dim2, 1))
            X = X * idf_tile
            X = X.reshape(dim1, dim2, dim3)

        print("forme des données d'entraînement : ", X.shape)
        return X

    def transform(self, X_seq):
        """
        Transforme l'ensemble de test en utilisant les paramètres calculés lors de l'entraînement.
        """
        time_images = []
        for block in X_seq:
            padded_block = sequence_padder(block, self.max_seq_length)
            time_image = windower(padded_block, self.window_size)
            time_image_counts = []
            for time_row in time_image:
                row_count = Counter(time_row)
                time_image_counts.append(row_count)

            time_image_df = pd.DataFrame(time_image_counts, columns=self.events)
            time_image_df = time_image_df.reindex(sorted(time_image_df.columns), axis=1)
            time_image_df = time_image_df.fillna(0)
            time_image_np = time_image_df.to_numpy()

            if len(time_image_np) > self.num_rows:
                time_image_np = resize_time_image(
                    time_image_np, (self.num_rows, len(self.events)),
                )

            time_images.append(time_image_np)

        X = np.stack(time_images)

        if self.term_weighting == "tf-idf":
            dim1, dim2, dim3 = X.shape
            X = X.reshape(-1, dim3)
            idf_tile = np.tile(self.idf_vec, (dim1 * dim2, 1))
            X = X * idf_tile
            X = X.reshape(dim1, dim2, dim3)

        print("forme des données de test : ", X.shape)
        return X


if __name__ == "__main__":

    test_data = "C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/parse/DataSet_HDFS/HDFS.log_structured.csv"

    df = pd.read_csv(test_data)

    re_pat = r"(blk_-?\d+)"
    col_names = ["BlockId", "EventSequence"]
    events_df = collect_event_ids(df, re_pat, col_names)

    test_df = events_df.head(100)

    print(test_df.head())

    print(test_df.shape)

    print(test_df["EventSequence"].values)
    lenghts = np.array(list(map(len, test_df["EventSequence"].values)))
    print(lenghts)

    print(max(lenghts))

    test_df.to_csv("C:/Users/LamiaLaraqui/Documents/FileSafe/Anomaly-Detection-Logs-DeepLearning-VSCode/Anomaly-Detection-Logs-DeepLearning/process/Datasets/test_frame.csv")
