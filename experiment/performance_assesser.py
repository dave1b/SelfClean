import concurrent.futures
import os
from pathlib import Path
from typing import Optional
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve

class PerformanceAssesser:
    def __init__(self, autocleaned_outliers, contamination_log):
        self.predictions: pd.DataFrame = autocleaned_outliers['data']
        self.meta_data: dict = autocleaned_outliers['metadata']
        self.contamination_log: pd.DataFrame = contamination_log
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
        self.roc_curve()
        # Print overview
        print(f"Total dataset size: {total_length}")
        print(f"True Positives: {self.tp}")
        print(f"False Positives: {self.fp}")
        print(f"False Negatives: {self.fn}")
        print(f"Precision: {self.precision:.4f}")

    def calculate_true_positives(self):
        print("Calculating true positives...")
        contamination_ids = set(self.contamination_log['id'].astype(str).dropna())
        contamination_pairs = set(zip(
            self.contamination_log['id_1'].astype(str),
            self.contamination_log['id_2'].astype(str)
        )) if {'id_1', 'id_2'}.issubset(self.contamination_log.columns) else set()

        positive_preds = self.predictions[self.predictions['prediction'] == True]
        # Vectorized check for single IDs
        tp_single = positive_preds[positive_preds['id'].notna() & positive_preds['id'].astype(str).isin(contamination_ids)].shape[0]
        # Vectorized check for pairs
        if {'id_1', 'id_2'}.issubset(positive_preds.columns):
            positive_preds_pairs = positive_preds[positive_preds['id'].isna()]
            tp_pairs = positive_preds_pairs.apply(
                lambda x: (str(x['id_1']), str(x['id_2'])) in contamination_pairs, axis=1
            ).sum()
        else:
            tp_pairs = 0
        self.tp = tp_single + tp_pairs
        return self.tp

    def calculate_false_positives(self):
        print("Calculating false positives...")
        contamination_ids = set(self.contamination_log['id'].astype(str).dropna())
        contamination_id1 = set(self.contamination_log['id_1'].astype(str)) if 'id_1' in self.contamination_log else set()
        contamination_id2 = set(self.contamination_log['id_2'].astype(str)) if 'id_2' in self.contamination_log else set()

        positive_preds = self.predictions[self.predictions['prediction'] == True]
        # Vectorized check for single IDs
        fp_single = positive_preds[positive_preds['id'].notna() & ~positive_preds['id'].astype(str).isin(contamination_ids)].shape[0]
        # Vectorized check for pairs
        if {'id_1', 'id_2'}.issubset(positive_preds.columns):
            positive_preds_pairs = positive_preds[positive_preds['id'].isna()]
            fp_pairs = positive_preds_pairs.apply(
                lambda x: str(x['id_1']) not in contamination_id1 and str(x['id_2']) not in contamination_id2, axis=1
            ).sum()
        else:
            fp_pairs = 0
        self.fp = fp_single + fp_pairs
        return self.fp

    def calculate_false_negatives(self):
        """
        Highly optimized false negative calculation using set operations.
        """
        print("Calculating false negatives...")

        # Get all positive predictions
        true_pred = self.predictions[self.predictions['prediction'] == True]

        # Prepare contamination data
        contam_has_id = self.contamination_log['id'].notna()
        contam_ids = set(self.contamination_log.loc[contam_has_id, 'id'].astype(str))
        contam_pairs = set(zip(
            self.contamination_log.loc[~contam_has_id, 'id_1'].astype(str),
            self.contamination_log.loc[~contam_has_id, 'id_2'].astype(str)
        ))

        # Prepare prediction data
        pred_ids = set(true_pred['id'].astype(str)) if 'id' in true_pred.columns else set()
        pred_pairs = set(zip(
            true_pred['id_1'].astype(str),
            true_pred['id_2'].astype(str)
        )) if {'id_1', 'id_2'}.issubset(true_pred.columns) else set()

        # Calculate false negatives using set differences
        fn_single = len(contam_ids - pred_ids) if contam_ids else 0
        fn_pairs = len(contam_pairs - pred_pairs) if contam_pairs else 0

        false_negatives = fn_single + fn_pairs
        self.fn = false_negatives
        return false_negatives

    def calculate_mean_average_precision(self):
        print("Calculating mean average precision...")
        if self.tp + self.fp == 0:
            self.precision = 0.0
        else:
            self.precision = self.tp / (self.tp + self.fp)
        return self.precision

    def roc_curve(self):
        cpu_count = os.cpu_count()

        print(f"Calculating AUC-ROC... with parallelism={cpu_count}")
        contamination_ids = set(self.contamination_log['id'].dropna().astype(str))
        contamination_pairs = set(
            zip(
                self.contamination_log['id_1'].astype(str),
                self.contamination_log['id_2'].astype(str)
            )
        )

        def is_contaminated(row):
            return (
                str(row['id']) in contamination_ids or
                (str(row['id_1']), str(row['id_2'])) in contamination_pairs
            )

        # Split the DataFrame into chunks for parallel processing
        chunk_size = 1_000_000  # Adjust based on your memory and system
        chunks = [
            self.predictions[i:i + chunk_size]
            for i in range(0, len(self.predictions), chunk_size)
        ]

        # Parallelize the label assignment
        with concurrent.futures.ThreadPoolExecutor(max_workers= cpu_count // 2) as executor:
            # Submit all chunks for parallel processing
            futures = [
                executor.submit(
                    lambda chunk=chunk: chunk.apply(is_contaminated, axis=1)
                )
                for chunk in chunks
            ]
            # Combine results as they complete
            labels = pd.concat([f.result() for f in concurrent.futures.as_completed(futures)])

        scores = 1 - self.predictions['score']
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
            output_path_ = output_path.with_suffix('.png')
            counter = 1
            while output_path_.exists():
                output_path_ = output_path.with_stem(f"{output_path.stem.split('_')[0]}_{counter}_roc").with_suffix('.png')
                counter += 1
            plt.savefig(output_path_)
            print(f"Issue scores saved to {output_path_}")
        plt.close()
