from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

class CodeBERTAnalyzer:
    def __init__(self, model_name="microsoft/codebert-base", num_labels=3):
        self.tokenizer = RobertaTokenizer.from_pretrained(model_name)
        self.model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

        # Optional: Load fine-tuned weights if available
        # self.model.load_state_dict(torch.load("codebert_tf_model.pt"))

        self.label_map = {
            0: "None",
            1: "Best Practice",
            2: "Security Risk"
        }

    def analyze(self, code: str) -> str:
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
        return self.label_map[predicted_class]
