import logging
import base64
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import pandas as pd

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def limpar_html(texto: str) -> str:
    """Remove tags HTML do texto."""
    soup = BeautifulSoup(texto, "html.parser")
    return soup.get_text()

def decodificar_corpo_email(payload: Dict[str, Any]) -> str:
    """Decodifica o corpo do e-mail da API Gmail."""
    if 'data' in payload:
        return base64.urlsafe_b64decode(payload['data']).decode('utf-8')
    return 'Corpo do e-mail não disponível'

def verificar_arquivos_essenciais():
    """Verifica se os arquivos necessários existem."""
    from .constants import CREDENTIALS_FILE, MODEL_PATH
    
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
    
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")