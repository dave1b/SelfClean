# Category Errors

| Model                        |     AP |   AUROC | Pooling Type       |
|------------------------------|--------|---------|--------------------|
| golden_swag_train_simcse_35  | 0.2825 |  0.7091 | mean_pooling       |
| golden_swag_train_simcse_35  | 0.2804 |  0.7055 | cls                |
| golden_swag_train_simcse_35  | 0.2802 |  0.7059 | first_last_average |
| golden_swag_train_simcse_35  | 0.2794 |  0.7084 | max                |
| deberta                      | 0.2705 |  0.6794 | max                |
| golden_swag_train_mlm_35     | 0.2544 |  0.6176 | mean_pooling       |
| golden_swag_train_mae_35     | 0.2444 |  0.6261 | mean_pooling       |
| golden_swag_train_mlm_35     | 0.2417 |  0.5999 | max                |
| deberta                      | 0.237  |  0.6711 | mean_pooling       |
| golden_swag_train_mae_35     | 0.235  |  0.6226 | first_last_average |
| golden_swag_train_mae_35     | 0.2342 |  0.622  | cls                |
| golden_swag_train_mae_35     | 0.2334 |  0.6167 | max                |
| deberta                      | 0.2167 |  0.6456 | first_last_average |
| deberta                      | 0.2164 |  0.6454 | cls                |
| golden_swag_train_mlm_35     | 0.2124 |  0.5816 | cls                |
| golden_swag_train_mlm_35     | 0.2123 |  0.5819 | first_last_average |
| bert                         | 0.1448 |  0.6002 | mean_pooling       |
| bert                         | 0.1394 |  0.5816 | first_last_average |
| bert                         | 0.1393 |  0.5831 | cls                |
| bert                         | 0.1383 |  0.5836 | max                |
| golden_swag_train_electra_35 | 0.1351 |  0.5589 | cls                |
| golden_swag_train_electra_35 | 0.1344 |  0.5584 | first_last_average |
| golden_swag_train_electra_35 | 0.1326 |  0.5551 | max                |
| golden_swag_train_electra_35 | 0.132  |  0.5431 | mean_pooling       |
| electra                      | 0.1296 |  0.5543 | cls                |
| electra                      | 0.1295 |  0.5534 | first_last_average |
| electra                      | 0.1275 |  0.5361 | mean_pooling       |
| electra                      | 0.127  |  0.5556 | max                |