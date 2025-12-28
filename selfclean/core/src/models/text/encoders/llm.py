from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForMaskedLM, ElectraForPreTraining, ElectraForMaskedLM


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

def electra():
    discriminator = ElectraForPreTraining.from_pretrained("google/electra-base-discriminator")
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return discriminator, tokenizer

############################################### SimCSE
def golden_swag_train_simcse_bert_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_12():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch12')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_25():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch25')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_NEAR_DUPLICATES_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def golden_swag_train_simcse_bert_NEAR_DUPLICATES_12():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch12')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def golden_swag_train_simcse_bert_NEAR_DUPLICATES_25():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch25')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q_12():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch12')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q_25():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/near_duplicate_question/epoch25')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_OFF_TOPIC_12():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch12')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_OFF_TOPIC_25():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/off_topic/epoch25')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

############################################### Electra
def golden_swag_train_electra_bert_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_25():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch25')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_50():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch50')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_25():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch25')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_50():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate/epoch50')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_Q_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_Q_25():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch25')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_NEAR_DUPLICATE_Q_50():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/near_duplicate_question/epoch50')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer


def golden_swag_train_electra_bert_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch1')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_OFF_TOPIC_25():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch25')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

def golden_swag_train_electra_bert_OFF_TOPIC_50():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/off_topic/epoch50')
    tokenizer = AutoTokenizer.from_pretrained("google/electra-base-discriminator")
    return model, tokenizer

############################################### MAE
def golden_swag_train_mae_bert_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_17():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch17')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/epoch35')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_17():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch17')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate/epoch35')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_Q_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_Q_17():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch17')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_NEAR_DUPLICATE_Q_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/near_duplicate_question/epoch35')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_OFF_TOPIC_1():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_OFF_TOPIC_17():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch17')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_mae_bert_OFF_TOPIC_35():
    model = AutoModel.from_pretrained('models/Mae_golden_swag_train/off_topic/epoch35')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer
