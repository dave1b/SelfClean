from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForMaskedLM, ElectraForPreTraining


def bert():
    model = AutoModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer

def pretrained_bert_mae():
    model = AutoModel.from_pretrained('models/MaeSimCSE')
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
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    return model, tokenizer

def electra():
    tokenizer = AutoTokenizer.from_pretrained('google/electra-base-discriminator')
    model = ElectraForPreTraining.from_pretrained('google/electra-small-discriminator')
    # model = AutoModel.from_pretrained('google/electra-base-discriminator')
    return model, tokenizer
