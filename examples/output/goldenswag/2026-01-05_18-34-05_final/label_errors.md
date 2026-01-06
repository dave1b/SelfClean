# Label Errors

| Model                        |     AP |   AUROC | Pooling Type       |
|------------------------------|--------|---------|--------------------|
| electra                      | 0.0815 |  0.639  | first_last_average |
| electra                      | 0.0813 |  0.6378 | cls                |
| electra                      | 0.0813 |  0.6229 | max                |
| golden_swag_train_electra_35 | 0.0801 |  0.6354 | first_last_average |
| golden_swag_train_electra_35 | 0.08   |  0.6339 | cls                |
| golden_swag_train_electra_35 | 0.0796 |  0.6204 | max                |
| deberta                      | 0.0776 |  0.5964 | max                |
| electra                      | 0.076  |  0.6326 | mean_pooling       |
| golden_swag_train_electra_35 | 0.0748 |  0.6255 | mean_pooling       |
| bert                         | 0.0747 |  0.6056 | max                |
| deberta                      | 0.0716 |  0.5919 | mean_pooling       |
| bert                         | 0.0715 |  0.6043 | mean_pooling       |
| golden_swag_train_simcse_35  | 0.0704 |  0.57   | first_last_average |
| bert                         | 0.0704 |  0.5988 | first_last_average |
| golden_swag_train_mlm_35     | 0.0704 |  0.6063 | mean_pooling       |
| golden_swag_train_simcse_35  | 0.0704 |  0.5701 | cls                |
| bert                         | 0.0703 |  0.5987 | cls                |
| deberta                      | 0.0693 |  0.5803 | cls                |
| deberta                      | 0.0692 |  0.5793 | first_last_average |
| golden_swag_train_mae_35     | 0.069  |  0.5885 | max                |
| golden_swag_train_mae_35     | 0.0685 |  0.5825 | cls                |
| golden_swag_train_mae_35     | 0.0684 |  0.5822 | first_last_average |
| golden_swag_train_simcse_35  | 0.0682 |  0.5665 | max                |
| golden_swag_train_mlm_35     | 0.0681 |  0.6017 | cls                |
| golden_swag_train_simcse_35  | 0.068  |  0.5664 | mean_pooling       |
| golden_swag_train_mlm_35     | 0.068  |  0.6018 | first_last_average |
| golden_swag_train_mae_35     | 0.0674 |  0.5795 | mean_pooling       |
| golden_swag_train_mlm_35     | 0.0653 |  0.5817 | max                |