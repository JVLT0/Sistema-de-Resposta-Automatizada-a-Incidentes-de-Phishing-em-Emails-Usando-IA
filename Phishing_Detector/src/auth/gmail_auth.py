from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

# Configurações atualizadas
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
BASE_DIR = Path(__file__).parent.parent.parent  # Ajuste conforme necessário
CONFIG_DIR = BASE_DIR / 'config'
TOKENS_DIR = BASE_DIR / 'auth_tokens'

def criar_servico(usuario="default"):
    """Autentica um usuário específico e retorna o serviço Gmail"""
    # Garante que os diretórios existem
    TOKENS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(exist_ok=True)
    
    # Caminhos dos arquivos
    client_secret_path = CONFIG_DIR / 'client_secret.json'
    token_path = TOKENS_DIR / f'{usuario}_token.json'

    if not client_secret_path.exists():
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {client_secret_path}")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret_path),
                SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)