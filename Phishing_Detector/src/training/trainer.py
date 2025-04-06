import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from transformers import BertForSequenceClassification
from typing import Tuple  # Importação adicionada para Tuple
import logging
from src.core.constants import MODEL_PATH
from src.core.constants import BATCH_SIZE, EPOCHS, LEARNING_RATE, device
from src.core.utils import logger

class TreinadorBERT:
    def __init__(
        self,
        model: BertForSequenceClassification,
        train_dataset: Dataset,
        val_dataset: Dataset,
        batch_size: int = BATCH_SIZE,
        epochs: int = EPOCHS,
        lr: float = LEARNING_RATE
    ):
        self.model = model.to(device)
        self.batch_size = batch_size
        self.epochs = epochs
        
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=lr)

    def treinar(self) -> None:
        """Executa o treinamento do modelo."""
        logger.info("Iniciando treinamento do BERT...")
        
        for epoch in range(self.epochs):
            self.model.train()
            total_loss = 0.0
            
            for batch in self.train_loader:
                self.optimizer.zero_grad()
                
                inputs = {
                    'input_ids': batch['input_ids'].to(device),
                    'attention_mask': batch['attention_mask'].to(device),
                    'labels': batch['label'].to(device)
                }
                
                outputs = self.model(**inputs)
                loss = outputs.loss
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(self.train_loader)
            logger.info(f"Época {epoch + 1}/{self.epochs}, Loss: {avg_loss:.4f}")
            self.avaliar()

        try:
            # Garante que o diretório existe
            MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            # Salva o modelo
            torch.save(self.model.state_dict(), str(MODEL_PATH))
            logger.info(f"Modelo salvo com sucesso em: {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Falha ao salvar modelo: {str(e)}")
            raise

    def avaliar(self) -> Tuple[float, float]:
        """Avalia o modelo no conjunto de validação."""
        self.model.eval()
        total_loss, correct = 0.0, 0
        total = 0
        
        with torch.no_grad():
            for batch in self.val_loader:
                inputs = {
                    'input_ids': batch['input_ids'].to(device),
                    'attention_mask': batch['attention_mask'].to(device),
                    'labels': batch['label'].to(device)
                }
                
                outputs = self.model(**inputs)
                loss = outputs.loss
                total_loss += loss.item()
                
                preds = torch.argmax(outputs.logits, dim=1)
                correct += (preds == inputs['labels']).sum().item()
                total += inputs['labels'].size(0)
        
        accuracy = 100 * correct / total
        avg_loss = total_loss / len(self.val_loader)
        
        logger.info(f"Validação - Loss: {avg_loss:.4f}, Acurácia: {accuracy:.2f}%")
        return avg_loss, accuracy