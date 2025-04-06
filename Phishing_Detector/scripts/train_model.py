import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.training.trainer import TreinadorBERT
from src.training.dataset import EmailDataset
from src.core.constants import DATA_DIR, MODEL_PATH
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
import logging

def main():
    try:
        # 1. Carregar dataset
        df = pd.read_csv(DATA_DIR / "dataset_emails.csv")
        
        # 2. Inicializar componentes
        tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        model = BertForSequenceClassification.from_pretrained(
            'neuralmind/bert-base-portuguese-cased',
            num_labels=2
        )
        
        # 3. Preparar dataset
        dataset = EmailDataset(df, tokenizer, max_length=256)
        
        # 4. Executar treinamento
        treinador = TreinadorBERT(
            model=model,
            train_dataset=dataset,  # Em produção, divida em train/val
            val_dataset=dataset     # Simplificado para exemplo
        )
        treinador.treinar()
        
        logging.info(f"Modelo treinado e salvo em {MODEL_PATH}")
    
    except Exception as e:
        logging.error(f"Erro no treinamento: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()