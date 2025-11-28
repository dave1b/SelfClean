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
