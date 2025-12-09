from pathlib import Path
from typing import Optional

import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.metrics import roc_auc_score, roc_curve


class PerformanceAssesser:
    def __init__(self, autocleaned_outliers, contamination_log):
        self.predictions: DataFrame = autocleaned_outliers['data']
        self.meta_data: dict = autocleaned_outliers['metadata']
        self.contamination_log: DataFrame = contamination_log
        self.tp = None
        self.fp = None
        self.fn = None
        self.tn = None
        self.precision = None
        output_folder = f"{self.meta_data['dataset_name']}_{self.meta_data['pretraining_type']}".lower()
        self.output_path: Optional[Path] = Path(__file__).parent.parent / "examples" / "output" / output_folder / "result_roc"

    def assess_performance(self):
        print("Assessing performance of auto-cleaning...")
        total_length = self.meta_data['dataset_size']

        self.calculate_true_positives()
        self.calculate_false_positives()
        self.calculate_false_negatives()
        self.calculate_mean_average_precision()
        self.plot_roc_curve()

        # print overview
        print(f"Total dataset size: {total_length}")
        print(f"True Positives: {self.tp}")
        print(f"False Positives: {self.fp}")
        print(f"False Negatives: {self.fn}")
        print(f"Precision: {self.precision:.4f}")

    def calculate_true_positives(self):
        """
        Calculate the number of true positives (correctly identified issues).
        Only considers entries where prediction=True.
        """
        true_positives = 0
        for _, pred in self.predictions[self.predictions['prediction'] == True].iterrows():
            if pred['id']:
                if pred['id'] in self.contamination_log['id'].astype(str).values:
                    true_positives += 1
            else:
                if pred['id_1'] in self.contamination_log['id_1'].astype(str).values and pred['id_2'] in self.contamination_log[
                    'id_2'].astype(str).values:
                    true_positives += 1
        self.tp = true_positives
        return true_positives

    def calculate_false_positives(self):
        """
        Calculate the number of false positives (incorrectly identified issues).
        Only considers entries where prediction=True.
        """
        false_positives = 0
        for _, pred in self.predictions[self.predictions['prediction'] == True].iterrows():
            if pred['id']:
                if pred['id'] not in self.contamination_log['id'].astype(str).values:
                    false_positives += 1
            else:
                if pred['id_1'] not in self.contamination_log['id_1'].astype(str).values and pred['id_2'] not in self.contamination_log[
                    'id_2'].astype(
                    str).values:
                    false_positives += 1
        self.fp = false_positives
        return false_positives

    def calculate_false_negatives(self):
        """
        Calculate the number of false negatives (missed issues).
        """
        true_pred = self.predictions[self.predictions['prediction'] == True]
        true_pred_id = true_pred['id_1'].astype(str).values
        true_pred_id_1 = true_pred['id_1'].astype(str).values
        true_pred_id_2 = true_pred['id_2'].astype(str).values

        false_negatives = 0
        for _, record in self.contamination_log.iterrows():
            if record['id'] and not pd.isna(record['id']):
                if str(record['id']) not in true_pred_id:
                    false_negatives += 1
            else:
                if str(record['id_1']) not in true_pred_id_1 and str(record['id_2']) not in true_pred_id_2:
                    false_negatives += 1
        self.fn = false_negatives
        return false_negatives

    def calculate_mean_average_precision(self):
        if self.tp + self.fp == 0:
            self.precision = 0.0
        else:
            self.precision = self.tp / (self.tp + self.fp)
        return self.precision

    def plot_roc_curve(self):
        """
        Plots the AUC-ROC (Area Under the Receiver Operating Characteristic Curve)
        Measures how well the model differentiates between classes.
        """
        labels = []
        scores = []

        for _, outlier in self.predictions.iterrows():
            # Check if this outlier is actually contaminated
            if outlier.get('id'):
                is_contaminated = not self.contamination_log[self.contamination_log['id'] == outlier['id']].empty
            else:
                is_contaminated = not self.contamination_log[
                    (self.contamination_log['id_1'] == outlier['id_1']) &
                    (self.contamination_log['id_2'] == outlier['id_2'])
                    ].empty

            labels.append(1 if is_contaminated else 0)
            scores.append(1 - outlier['score'])  # Use inverse of score as detection confidence

        fpr, tpr, thresholds = roc_curve(labels, scores)
        auc = roc_auc_score(labels, scores)

        plt.figure(figsize=(7, 7))
        plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], color='gray', linestyle='--')

        for i in range(len(thresholds)):
            if i % max(1, len(thresholds) // 10) == 0:
                plt.scatter(fpr[i], tpr[i], color='red', s=40)
                plt.text(fpr[i] + 0.02, tpr[i] - 0.02, f'{thresholds[i]:.2f}', fontsize=8, color='black')

        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve with Threshold Markers')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        if self.output_path:
            output_path = Path(self.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Ensure unique filename
            output_path_ = output_path.with_suffix('.png')
            counter = 1
            while output_path_.exists():
                output_path_ = output_path.with_stem(f"{output_path.stem.split('_')[0]}_{counter}_roc").with_suffix('.png')
                counter += 1
            plt.savefig(output_path_)
            print(f"Issue scores saved to {output_path_}")
        plt.close()
