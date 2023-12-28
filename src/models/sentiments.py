from . import *

class Sentiment:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DistilBertForSequenceClassification.from_pretrained(self.model_name).to(self.device)

    def predict_sentiment(self, text: str) -> str:
        self.model.to(self.device)

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=128,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=-1).item()

        return ['NEGATIVE', 'NEUTRAL', 'POSITIVE'][predicted_class]