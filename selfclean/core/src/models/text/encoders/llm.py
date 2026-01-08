from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForMaskedLM, ElectraForPreTraining, ElectraForMaskedLM, \
    DebertaV2ForMaskedLM, AutoModelForMaskedLM


def bert():
    model = AutoModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def roberta():
    model = AutoModel.from_pretrained('roberta-base')
    tokenizer = AutoTokenizer.from_pretrained('roberta-base')
    return model, tokenizer

def deberta():
    model = AutoModel.from_pretrained('microsoft/deberta-v3-base')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def distilbert():
    model = AutoModel.from_pretrained('distilbert/distilbert-base-uncased-finetuned-sst-2-english')
    tokenizer = AutoTokenizer.from_pretrained('distilbert/distilbert-base-uncased-finetuned-sst-2-english')
    return model, tokenizer

def bert_mlm():
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def deberta_mlm():
    model = DebertaV2ForMaskedLM.from_pretrained('microsoft/deberta-v3-base')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def electra():
    discriminator = AutoModel.from_pretrained("google/electra-base-discriminator")
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return discriminator, tokenizer

def electra_electra():
    discriminator = ElectraForPreTraining.from_pretrained("google/electra-base-discriminator")
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return discriminator, tokenizer

def hella_swag_electra():
    discriminator = AutoModel.from_pretrained("models/Electra_hella_swag/epoch30")
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return discriminator, tokenizer

def hella_swag_simcse():
    discriminator = AutoModel.from_pretrained("models/SimCSE_hella_swag/epoch16")
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return discriminator, tokenizer


############################################### SimCSE
# General models
def golden_swag_train_simcse_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_10():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_20():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_35():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates models
def golden_swag_train_simcse_NEAR_DUPLICATES_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_10():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_20():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_35():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates in questions models
def golden_swag_train_simcse_NEAR_DUPLICATES_Q_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_Q_10():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_Q_20():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_NEAR_DUPLICATES_Q_35():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Off-topic models
def golden_swag_train_simcse_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_OFF_TOPIC_10():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_OFF_TOPIC_20():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_simcse_OFF_TOPIC_35():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

############################################### Electra
# General models
def golden_swag_train_electra_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_10():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch10')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_20():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch20')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_35():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch35')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

# General models without weight sharing
def golden_swag_train_electra_w_weight_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/default_w_weights_sharing/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_w_weight_10():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/default_w_weights_sharing/epoch10')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_w_weight_20():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/default_w_weights_sharing/epoch20')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_w_weight_35():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/default_w_weights_sharing/epoch35')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

# Near duplicates models
def golden_swag_train_electra_NEAR_DUPLICATE_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_10():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch10')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_20():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch20')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_35():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch35')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

# Near duplicates in questions models
def golden_swag_train_electra_NEAR_DUPLICATE_Q_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_Q_10():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch10')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_Q_20():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch20')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_NEAR_DUPLICATE_Q_35():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch35')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

# Off-topic models
def golden_swag_train_electra_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_OFF_TOPIC_10():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch10')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_OFF_TOPIC_20():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch20')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_OFF_TOPIC_35():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch35')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

############################################### MAE
# General models
def golden_swag_train_mae_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_10():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_20():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates models
def golden_swag_train_mae_NEAR_DUPLICATE_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_10():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_20():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates in questions models
def golden_swag_train_mae_NEAR_DUPLICATE_Q_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_Q_10():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_Q_20():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_NEAR_DUPLICATE_Q_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Off-topic models
def golden_swag_train_mae_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_OFF_TOPIC_10():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_OFF_TOPIC_20():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mae_OFF_TOPIC_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer


############################################### MLM
# General models
def golden_swag_train_mlm_1():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_10():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_20():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_35():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates models
def golden_swag_train_mlm_NEAR_DUPLICATE_1():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_10():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_20():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_35():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Near duplicates in questions models
def golden_swag_train_mlm_NEAR_DUPLICATE_Q_1():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_Q_10():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate_question/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_Q_20():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate_question/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_NEAR_DUPLICATE_Q_35():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/near_duplicate_question/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

# Off-topic models
def golden_swag_train_mlm_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/off_topic/epoch1')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_OFF_TOPIC_10():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/off_topic/epoch10')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_OFF_TOPIC_20():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/off_topic/epoch20')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer

def golden_swag_train_mlm_OFF_TOPIC_35():
    model = AutoModel.from_pretrained('models/MLM_golden_swag_train/off_topic/epoch35')
    tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base')
    return model, tokenizer
