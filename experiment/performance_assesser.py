import numpy as np
from loguru import logger
import time
from pathlib import Path
from typing import Optional, Set, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import dask.dataframe as dd
from sklearn.metrics import roc_auc_score, roc_curve
from selfclean.core.src.utils.plotting import calculate_scores_from_ranking


class PerformanceAssesser:
    def __init__(self, prediction: dict, contamination_log: pd.DataFrame):
        self.predictions: dd.DataFrame = dd.read_parquet(prediction['data_path'])
        self.meta_data: dict = prediction['metadata']
        self.contamination_log: pd.DataFrame = contamination_log
        self.tp, self.fp, self.fn = None, None, None
        self.tn, self.auc, self.precision = None, None, None
        self.afe = None
        self.contamination_single_ids: Set[str] = set()
        self.contamination_pair_ids: Set[Tuple[str, str]] = set()
        self.log_dict: dict = {}
        self.ranked_labels: np.ndarray = np.array([])
        self.output_path: Optional[Path] = prediction['data_path'].parent
        self._has_pairs: bool = {'id_1', 'id_2'}.issubset(contamination_log.columns)
        self._has_single_id: bool = 'id' in contamination_log.columns

    def assess_performance(self) -> None:
        logger.info("Assessing performance of auto-cleaning...")
        self.plotting()
        self.export_results()

    def _prepare_contamination_ids(self) -> None:
        if self._has_single_id:
            self.contamination_single_ids = set(
                self.contamination_log['id'].astype(str).dropna()
            )
        if self._has_pairs:
            self.contamination_pair_ids = set(zip(
                self.contamination_log['id_1'].astype(str),
                self.contamination_log['id_2'].astype(str)
            ))

    def _calculate_metrics(self) -> None:
        positive_preds = self.predictions[self.predictions['prediction'] == True]
        self.tp = self._calculate_true_positives(positive_preds)
        self.fp = self._calculate_false_positives(positive_preds)
        self.fn = self._calculate_false_negatives()
        self.precision = self._calculate_precision()

    def _calculate_true_positives(self, positive_preds: dd.DataFrame) -> int:
        tp_single = 0
        if self._has_single_id:
            tp_single = positive_preds[
                positive_preds['id'].notnull() &
                positive_preds['id'].astype(str).isin(self.contamination_single_ids)
                ].shape[0].compute()

        tp_pairs = 0
        if self._has_pairs:
            positive_preds_pairs = positive_preds[positive_preds['id_1'].notnull()]
            pred_pairs = set(zip(
                positive_preds_pairs['id_1'].astype(str).compute(),
                positive_preds_pairs['id_2'].astype(str).compute()
            ))
            tp_pairs = len(pred_pairs & self.contamination_pair_ids)

        return tp_single + tp_pairs

    def _calculate_false_positives(self, positive_preds: dd.DataFrame) -> int:
        fp_single = 0
        if self._has_single_id:
            fp_single = positive_preds[
                positive_preds['id'].notnull() &
                ~positive_preds['id'].astype(str).isin(self.contamination_single_ids)
                ].shape[0].compute()

        fp_pairs = 0
        if self._has_pairs:
            positive_preds_pairs = positive_preds[positive_preds['id_1'].notnull()]
            pred_pairs = set(zip(
                positive_preds_pairs['id_1'].astype(str).compute(),
                positive_preds_pairs['id_2'].astype(str).compute()
            ))
            fp_pairs = len(pred_pairs - self.contamination_pair_ids)

        return fp_single + fp_pairs

    def _calculate_false_negatives(self) -> int:
        true_pred = self.predictions[self.predictions['prediction'] == True].compute()

        fn_single = 0
        if self._has_single_id:
            contam_ids = set(self.contamination_log['id'].astype(str).dropna())
            pred_ids = set(true_pred['id'].astype(str)) if 'id' in true_pred.columns else set()
            fn_single = len(contam_ids - pred_ids)

        fn_pairs = 0
        if self._has_pairs:
            contam_pairs = set(zip(
                self.contamination_log['id_1'].astype(str),
                self.contamination_log['id_2'].astype(str)
            ))
            pred_pairs = set(zip(
                true_pred['id_1'].astype(str),
                true_pred['id_2'].astype(str)
            )) if {'id_1', 'id_2'}.issubset(true_pred.columns) else set()
            fn_pairs = len(contam_pairs - pred_pairs)

        return fn_single + fn_pairs

    def _calculate_precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0

    def _calculate_ranked_labels(self) -> None:
        logger.info("Calculating ranked labels...")
        if self._has_single_id:
            contamination_ids = set(self.contamination_log['id'].astype(str).dropna())
            self.ranked_labels = self.predictions['id'].astype(str).isin(contamination_ids)
        else:
            contamination_index = pd.MultiIndex.from_arrays([
                self.contamination_log['id_1'].astype(str),
                self.contamination_log['id_2'].astype(str)
            ])
            pred_index = pd.MultiIndex.from_arrays([
                self.predictions['id_1'].astype(str).compute(),
                self.predictions['id_2'].astype(str).compute()
            ])
            self.ranked_labels = pred_index.isin(contamination_index)
        if self.output_path:
            path = self.output_path / "ranked_labels"
            packed = np.packbits(self.ranked_labels)
            np.save(path, packed)

    def _calculate_fraction_of_effort(self) -> None:
        """
        Calculate Fraction of Effort (FoE) for different inspection thresholds.
        FoE measures what fraction of all contaminated samples can be found by inspecting
        only the top-k samples ranked by contamination likelihood.

        For HellaSwag/SelfClean, this shows how much human effort is reduced by using
        the model's predictions to prioritize inspection.
        """
        logger.info("Calculating Fraction of Effort (FoE)...")

        scores = self.predictions['score'].compute()
        labels = self.ranked_labels

        combined = list(zip(scores, labels))
        combined_sorted = sorted(combined, key=lambda x: x[0], reverse=True)  # High score first
        sorted_scores, sorted_labels = zip(*combined_sorted)
        sorted_labels = np.array(sorted_labels)

        cumulative_contaminated = np.cumsum(sorted_labels)
        total_contamination = cumulative_contaminated[-1]  # Total contaminated samples

        if total_contamination == 0:
            logger.warning("No contaminated samples found in the data. FoE calculation aborted.")
            return

        total_samples = len(sorted_labels)

        k_values = np.arange(1, total_samples + 1)
        foe_curve = cumulative_contaminated / total_contamination

        self.log_dict['total_contamination'] = total_contamination

        # Calculate area under FoE curve (additional metric)
        foe_auc = np.trapz(foe_curve, k_values) / total_samples
        self.afe = foe_auc
        self.log_dict['foe_auc'] = round(foe_auc, 4)

    def plotting(self) -> None:
        self._calculate_ranked_labels()
        self._calculate_fraction_of_effort()  # Add this line
        calculate_scores_from_ranking(self.ranked_labels, path=self.output_path, log_dict=self.log_dict, show_plots=False, save_plots=True)

    def roc_curve(self) -> None:
        logger.info("Calculating AUC-ROC...")
        start_time = time.time()
        labels = self.ranked_labels
        scores = 1 - self.predictions['score'].compute()

        fpr, tpr, thresholds = roc_curve(labels, scores)
        self.auc = roc_auc_score(labels, scores)

        plt.figure(figsize=(7, 7))
        plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {self.auc:.3f})')
        plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
        for i in range(0, len(thresholds), max(1, len(thresholds) // 10)):
            plt.scatter(fpr[i], tpr[i], color='red', s=40)
            plt.text(fpr[i] + 0.02, tpr[i] - 0.02, f'{thresholds[i]:.2f}', fontsize=8, color='black')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve with Threshold Markers')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        if self.output_path:
            output_path = Path(self.output_path) / "result_roc.png"
            plt.savefig(output_path)
            logger.info(f"ROC plot saved to {output_path}")
        plt.close()
        logger.info(f"Calculated ROC in {(time.time() - start_time) / 60:.2f} minutes, AUC: {self.auc:.4f}")

    def export_results(self) -> None:
        df = pd.DataFrame([self.log_dict])
        if self.output_path:
            path = Path(self.output_path) / "result_metrics.csv"
            df.to_csv(path, index=False)

    def _log_results(self, total_length: int) -> None:
        logger.info("\nPerformance Assessment Results:")
        logger.info(f" Total dataset size: {total_length}")
        logger.info(f" True Positives: {self.tp}")
        logger.info(f" False Positives: {self.fp}")
        logger.info(f" False Negatives: {self.fn}")
        logger.info(f" Precision: {self.precision:.4f}")
        logger.info(f" Average Fraction of Effort: {self.afe:.4f}")
