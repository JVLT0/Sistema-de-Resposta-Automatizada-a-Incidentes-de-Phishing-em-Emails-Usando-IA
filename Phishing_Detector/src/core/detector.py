import torch
import logging
from transformers import BertTokenizer, BertForSequenceClassification
from typing import List

from src.core.constants import MODEL_PATH, MAX_LENGTH, THRESHOLD, device
from src.core.utils import logger

class DetectorPhishing:
    def __init__(self):
        self.device = device
        self.tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.model = self._carregar_modelo()
    
    def _carregar_modelo(self) -> BertForSequenceClassification:
        """Carrega o modelo BERT pré-treinado."""
        model = BertForSequenceClassification.from_pretrained(
            'neuralmind/bert-base-portuguese-cased',
            num_labels=2
        ).to(self.device)
        
        model.load_state_dict(torch.load(str(MODEL_PATH), map_location=self.device))
        model.eval()
        return model
    
    def prever(self, emails_df) -> List[int]:
        """Executa a detecção de phishing nos e-mails."""
        logger.info("Executando detecção de phishing...")
        textos = (emails_df['assunto'] + " " + emails_df['conteudo']).tolist()
        
        encodings = self.tokenizer(
            textos, 
            truncation=True, 
            padding=True, 
            max_length=MAX_LENGTH, 
            return_tensors='pt'
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(
                encodings['input_ids'], 
                attention_mask=encodings['attention_mask']
            )
            probabilidades = torch.nn.functional.softmax(outputs.logits, dim=1)
            previsoes = (probabilidades[:, 1] > THRESHOLD).int()
        
        return previsoes.cpu().numpy().tolist()