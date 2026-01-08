# Label Errors

| Model                        |     AP |   AUROC | Pooling Type   |
|------------------------------|--------|---------|----------------|
| electra                      | 0.076  |  0.6326 | mean_pooling   |
| golden_swag_train_electra_35 | 0.0748 |  0.6255 | mean_pooling   |
| deberta                      | 0.0716 |  0.5919 | mean_pooling   |
| bert                         | 0.0715 |  0.6043 | mean_pooling   |
| golden_swag_train_mlm_35     | 0.0704 |  0.6063 | mean_pooling   |
| golden_swag_train_simcse_35  | 0.068  |  0.5664 | mean_pooling   |
| golden_swag_train_mae_35     | 0.0674 |  0.5795 | mean_pooling   |