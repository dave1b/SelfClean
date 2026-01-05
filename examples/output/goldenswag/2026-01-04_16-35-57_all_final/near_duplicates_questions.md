# Near Duplicates Questions

| Model                                         |     AP |   AUROC | Pooling Type       |
|-----------------------------------------------|--------|---------|--------------------|
| bert                                          | 0.8177 |  0.9603 | max                |
| bert                                          | 0.7386 |  0.9956 | mean_pooling       |
| golden_swag_train_electra_NEAR_DUPLICATE_Q_35 | 0.5301 |  0.9918 | mean_pooling       |
| bert                                          | 0.485  |  0.9902 | cls                |
| electra                                       | 0.4687 |  0.9394 | max                |
| golden_swag_train_electra_NEAR_DUPLICATE_Q_35 | 0.4633 |  0.9396 | max                |
| bert                                          | 0.4611 |  0.9904 | first_last_average |
| electra                                       | 0.4339 |  0.9822 | mean_pooling       |
| golden_swag_train_electra_NEAR_DUPLICATE_Q_35 | 0.27   |  0.9398 | first_last_average |
| golden_swag_train_electra_NEAR_DUPLICATE_Q_35 | 0.2677 |  0.9348 | cls                |
| electra                                       | 0.2462 |  0.9129 | first_last_average |
| electra                                       | 0.2411 |  0.9092 | cls                |
| golden_swag_train_mae_NEAR_DUPLICATE_Q_35     | 0.0012 |  0.7747 | max                |
| golden_swag_train_mae_NEAR_DUPLICATE_Q_35     | 0.0012 |  0.7732 | mean_pooling       |
| golden_swag_train_mlm_NEAR_DUPLICATE_Q_35     | 0.001  |  0.6921 | max                |
| golden_swag_train_mae_NEAR_DUPLICATE_Q_35     | 0.0009 |  0.7701 | cls                |
| golden_swag_train_mae_NEAR_DUPLICATE_Q_35     | 0.0009 |  0.7712 | first_last_average |
| deberta                                       | 0.0008 |  0.6477 | first_last_average |
| deberta                                       | 0.0008 |  0.6747 | mean_pooling       |
| deberta                                       | 0.0008 |  0.6503 | cls                |
| golden_swag_train_mlm_NEAR_DUPLICATE_Q_35     | 0.0007 |  0.7221 | mean_pooling       |
| deberta                                       | 0.0006 |  0.6383 | max                |
| golden_swag_train_mlm_NEAR_DUPLICATE_Q_35     | 0.0004 |  0.7144 | cls                |
| golden_swag_train_mlm_NEAR_DUPLICATE_Q_35     | 0.0004 |  0.7146 | first_last_average |
| golden_swag_train_simcse_NEAR_DUPLICATES_Q_35 | 0.0003 |  0.7312 | max                |
| golden_swag_train_simcse_NEAR_DUPLICATES_Q_35 | 0.0003 |  0.7219 | mean_pooling       |
| golden_swag_train_simcse_NEAR_DUPLICATES_Q_35 | 0.0003 |  0.7151 | cls                |
| golden_swag_train_simcse_NEAR_DUPLICATES_Q_35 | 0.0003 |  0.714  | first_last_average |