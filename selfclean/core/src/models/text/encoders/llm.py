from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForMaskedLM, ElectraForPreTraining, ElectraForMaskedLM


def bert():
    model = AutoModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def pretrained_bert_hellaSwag_mae():
    model = AutoModel.from_pretrained('models/Mae_hellaSwag')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def pretrained_bert_hellaSwag_simcse():
    model = AutoModel.from_pretrained('models/SimCSE_hellaSwag')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def pretrained_bert_mmlu_mae():
    model = AutoModel.from_pretrained('models/Mae_mmlu')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def pretrained_bert_mmlu_simcse():
    model = AutoModel.from_pretrained('models/SimCSE_mmlu')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def roberta():
    model = AutoModel.from_pretrained('roberta-base')
    tokenizer = AutoTokenizer.from_pretrained('roberta-base')
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

def golden_swag_train_simcse_bert_4():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch4')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_8():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train/epoch8')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_NEAR_DUPLICATES_Q():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train_NEAR_DUPLICATES_Q')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_simcse_bert_NEAR_DUPLICATES():
    model = AutoModel.from_pretrained('models/SimCSE_golden_swag_train_NEAR_DUPLICATES')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

############################################### Electra
def golden_swag_train_electra_bert_1():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch1')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_electra_bert_6():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch6')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def golden_swag_train_electra_bert_22():
    model = AutoModel.from_pretrained('models/Electra_golden_swag_train/epoch22')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer
