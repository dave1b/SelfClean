# Near Duplicates

| Model                                       |     AP |   AUROC | Pooling Type       |
|---------------------------------------------|--------|---------|--------------------|
| golden_swag_train_electra_NEAR_DUPLICATE_35 | 0.5163 |  0.9989 | mean_pooling       |
| bert                                        | 0.5108 |  1      | mean_pooling       |
| electra                                     | 0.484  |  0.9986 | mean_pooling       |
| bert                                        | 0.4122 |  0.9999 | cls                |
| bert                                        | 0.4053 |  0.9999 | first_last_average |
| golden_swag_train_electra_NEAR_DUPLICATE_35 | 0.3772 |  0.9869 | first_last_average |
| bert                                        | 0.377  |  0.9999 | max                |
| golden_swag_train_electra_NEAR_DUPLICATE_35 | 0.3734 |  0.9866 | cls                |
| electra                                     | 0.3071 |  0.9875 | first_last_average |
| electra                                     | 0.304  |  0.9876 | cls                |
| golden_swag_train_electra_NEAR_DUPLICATE_35 | 0.1836 |  0.9939 | max                |
| electra                                     | 0.1719 |  0.9991 | max                |
| golden_swag_train_mae_NEAR_DUPLICATE_35     | 0.0193 |  0.9592 | cls                |
| golden_swag_train_mae_NEAR_DUPLICATE_35     | 0.0188 |  0.9596 | first_last_average |
| golden_swag_train_mae_NEAR_DUPLICATE_35     | 0.0178 |  0.9587 | max                |
| golden_swag_train_mae_NEAR_DUPLICATE_35     | 0.0156 |  0.9581 | mean_pooling       |
| golden_swag_train_mlm_NEAR_DUPLICATE_35     | 0.013  |  0.9723 | max                |
| golden_swag_train_mlm_NEAR_DUPLICATE_35     | 0.011  |  0.9746 | cls                |
| golden_swag_train_mlm_NEAR_DUPLICATE_35     | 0.011  |  0.9747 | first_last_average |
| golden_swag_train_mlm_NEAR_DUPLICATE_35     | 0.0075 |  0.9658 | mean_pooling       |
| deberta                                     | 0.0071 |  0.9096 | cls                |
| deberta                                     | 0.007  |  0.9091 | first_last_average |
| deberta                                     | 0.006  |  0.8914 | mean_pooling       |
| deberta                                     | 0.0049 |  0.8648 | max                |
| golden_swag_train_simcse_NEAR_DUPLICATES_35 | 0.0012 |  0.9316 | cls                |
| golden_swag_train_simcse_NEAR_DUPLICATES_35 | 0.0011 |  0.9338 | mean_pooling       |
| golden_swag_train_simcse_NEAR_DUPLICATES_35 | 0.0011 |  0.9303 | first_last_average |
| golden_swag_train_simcse_NEAR_DUPLICATES_35 | 0.0008 |  0.9376 | max                |