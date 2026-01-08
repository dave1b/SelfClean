# Label Errors

| Model                        |     AP |   AUROC | Pooling Type   |
|------------------------------|--------|---------|----------------|
| electra                      | 0.0813 |  0.6378 | cls            |
| golden_swag_train_electra_35 | 0.08   |  0.6339 | cls            |
| golden_swag_train_simcse_35  | 0.0704 |  0.5701 | cls            |
| bert                         | 0.0703 |  0.5987 | cls            |
| deberta                      | 0.0693 |  0.5803 | cls            |
| golden_swag_train_mae_35     | 0.0685 |  0.5825 | cls            |
| golden_swag_train_mlm_35     | 0.0681 |  0.6017 | cls            |