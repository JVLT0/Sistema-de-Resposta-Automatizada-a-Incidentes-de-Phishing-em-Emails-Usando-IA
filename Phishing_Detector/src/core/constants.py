import torch
from pathlib import Path

# Configuração de diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / 'config'
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'

# Configurações do dispositivo
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Arquivos de autenticação
CREDENTIALS_FILE = CONFIG_DIR / 'client_secret.json'
TOKEN_FILE = Path.home() / '.phishing_detector' / 'token.json'

# Modelo BERT
MODEL_PATH = MODELS_DIR / 'modelo_bert_phishing.pth'

# Garante que os diretórios existam
MODELS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

# Configurações do modelo
MAX_LENGTH = 256
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
EPOCHS = 3
THRESHOLD = 0.6  # Limiar para classificação de phishing

# Escopos da API Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']