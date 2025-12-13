from loguru import logger
import time
from pathlib import Path
from typing import Optional
import pandas as pd
from matplotlib import pyplot as plt
import dask.dataframe as dd
from sklearn.metrics import roc_auc_score, roc_curve


class PerformanceAssesser:
    def __init__(self, prediction, contamination_log):
        self.predictions: dd = dd.read_parquet(prediction['data_path'])
        self.meta_data: dict = prediction['metadata']
        self.contamination_log: pd.DataFrame = contamination_log
        self.tp = None
        self.fp = None
        self.fn = None
        self.tn = None
        self.precision = None
        self.auc = None
        self.output_path: Optional[Path] = prediction['data_path'].parent

    def assess_performance(self):
        logger.info("Assessing performance of auto-cleaning...")
        total_length = self.meta_data['dataset_size']
        self.calculate_true_positives()
        self.calculate_false_positives()
        self.calculate_false_negatives()
        self.calculate_mean_average_precision()
        self.roc_curve()
        self.export_results()
        # Print overview
        logger.info("Performance Assessment Results:")
        logger.info(f" Total dataset size: {total_length}")
        logger.info(f" True Positives: {self.tp}")
        logger.info(f" False Positives: {self.fp}")
        logger.info(f" False Negatives: {self.fn}")
        logger.info(f" Precision: {self.precision:.4f}")

    def export_results(self):
        metrics_df = pd.DataFrame([{
            'total_dataset_size': self.meta_data['dataset_size'],
            'true_positives': self.tp,
            'false_positives': self.fp,
            'false_negatives': self.fn,
            'precision': self.precision,
            'auc_roc': self.auc
        }])

        if self.output_path:
            path = Path(self.output_path / "result_metrics.csv")
            metrics_df.to_csv(path, index=False)

    def calculate_true_positives(self):
        logger.info("Calculating true positives...")
        contamination_ids = set(self.contamination_log['id'].astype(str).dropna())
        contamination_pairs = set(zip(
            self.contamination_log['id_1'].astype(str),
            self.contamination_log['id_2'].astype(str)
        )) if {'id_1', 'id_2'}.issubset(self.contamination_log.columns) else set()

        positive_preds = self.predictions[self.predictions['prediction'] == True]
        # Vectorized check for single IDs
        tp_single = positive_preds[positive_preds['id'].notnull() & positive_preds['id'].astype(str).isin(contamination_ids)].shape[0]
        # Vectorized check for pairs
        if {'id_1', 'id_2'}.issubset(positive_preds.columns):
            positive_preds_pairs = positive_preds[positive_preds['id'].notnull()]
            tp_pairs = positive_preds_pairs.apply(
                lambda x: (str(x['id_1']), str(x['id_2'])) in contamination_pairs, axis=1
            ).sum()
        else:
            tp_pairs = 0
        self.tp = (tp_single + tp_pairs).compute()
        return self.tp

    def calculate_false_positives(self):
        logger.info("Calculating false positives...")
        contamination_ids = set(self.contamination_log['id'].astype(str).dropna())
        contamination_id1 = set(self.contamination_log['id_1'].astype(str)) if 'id_1' in self.contamination_log else set()
        contamination_id2 = set(self.contamination_log['id_2'].astype(str)) if 'id_2' in self.contamination_log else set()

        positive_preds = self.predictions[self.predictions['prediction'] == True]
        # Vectorized check for single IDs
        fp_single = positive_preds[positive_preds['id'].notnull() & ~positive_preds['id'].astype(str).isin(contamination_ids)].shape[0]
        # Vectorized check for pairs
        if {'id_1', 'id_2'}.issubset(positive_preds.columns):
            positive_preds_pairs = positive_preds[positive_preds['id'].notnull()]
            fp_pairs = positive_preds_pairs.apply(
                lambda x: str(x['id_1']) not in contamination_id1 and str(x['id_2']) not in contamination_id2, axis=1
            ).sum()
        else:
            fp_pairs = 0
        self.fp = (fp_single + fp_pairs).compute()
        return self.fp

    def calculate_false_negatives(self):
        """
        Highly optimized false negative calculation using set operations.
        """
        logger.info("Calculating false negatives...")

        true_pred_ddf = self.predictions[self.predictions['prediction'] == True]
        true_pred = true_pred_ddf.compute()

        single_id_mask = self.contamination_log['id'].notna()

        contam_ids_df = self.contamination_log[single_id_mask]
        contam_ids = set(contam_ids_df['id'].astype(str))

        contam_pairs_df = self.contamination_log[~single_id_mask]
        contam_pairs = set(zip(
            contam_pairs_df['id_1'].astype(str),
            contam_pairs_df['id_2'].astype(str)
        ))

        if 'id' in true_pred.columns:
            pred_ids = set(true_pred['id'].astype(str))
        else:
            pred_ids = set()

        if {'id_1', 'id_2'}.issubset(true_pred.columns):
            pred_pairs = set(zip(
                true_pred['id_1'].astype(str),
                true_pred['id_2'].astype(str)
            ))
        else:
            pred_pairs = set()

        fn_single = len(contam_ids - pred_ids)
        fn_pairs = len(contam_pairs - pred_pairs)

        false_negatives = fn_single + fn_pairs
        self.fn = false_negatives
        logger.info(f"False Negatives calculated: {false_negatives} (Single: {fn_single}, Pair: {fn_pairs})")
        return false_negatives

    def calculate_mean_average_precision(self):
        logger.info("Calculating mean average precision...")
        if self.tp + self.fp == 0:
            self.precision = 0.0
        else:
            self.precision = self.tp / (self.tp + self.fp)
        return self.precision

    def roc_curve(self):
        logger.info(f"Calculating AUC-ROC...")
        start_time = time.time()
        contamination_ids = set(self.contamination_log['id'].dropna().astype(str))
        contamination_pairs = set(
            zip(
                self.contamination_log['id_1'].astype(str),
                self.contamination_log['id_2'].astype(str)
            )
        )

        def compute_label(partition_df):
            """
            Applies contamination check to a Pandas partition of the Dask DataFrame.
            Leverages NumPy/Pandas vectorization for speed inside the partition.
            """
            id_col = partition_df['id'].astype(str)
            id_pair_col = list(zip(
                partition_df['id_1'].astype(str),
                partition_df['id_2'].astype(str)
            ))

            # Vectorized check: faster than row-by-row apply
            is_id_contaminated = id_col.isin(contamination_ids)
            is_pair_contaminated = pd.Series([pair in contamination_pairs for pair in id_pair_col], index=partition_df.index)

            # Combine checks using the OR operator
            return is_id_contaminated | is_pair_contaminated

        logger.info("Calculating labels across Dask partitions...")

        # Use Dask's .apply() or .map_partitions()
        # .apply() is simpler here since we are applying a function across rows/columns.
        # The result is a Dask Series of boolean values (the labels)
        # The meta defines the output type (boolean Series)
        labels_dask = self.predictions.map_partitions(
            compute_label,
            meta=('labels', 'bool')
        )

        # --- 4. COLLECT SCORES AND LABELS (AND COMPUTE AUC) ---
        # The .compute() call is where Dask triggers parallel execution and brings
        # the final result into memory as a Pandas Series.
        # NOTE: This step is unavoidable, as sklearn needs the entire data array in memory.
        try:
            labels = labels_dask.compute()
            scores = 1 - self.predictions['score'].compute()
        except Exception as e:
            logger.error(f"Failed to compute Dask results. Ensure labels and scores fit in memory. Error: {e}")
            return None

        fpr, tpr, thresholds = roc_curve(labels, scores)
        self.auc = roc_auc_score(labels, scores)

        plt.figure(figsize=(7, 7))
        plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {self.auc:.3f})')
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
            output_path = Path(self.output_path / "result_roc")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path_ = output_path.with_suffix('.png')
            counter = 1
            while output_path_.exists():
                output_path_ = output_path.with_stem(f"{output_path.stem.split('_')[0]}_{counter}_roc").with_suffix('.png')
                counter += 1
            plt.savefig(output_path_)
            logger.info(f"ROC plot saved to {output_path_}")
        plt.close()
        logger.info(f"Calculated ROC in {(time.time() - start_time) / 60:.2f} minutes, AUC: {self.auc:.4f}")
