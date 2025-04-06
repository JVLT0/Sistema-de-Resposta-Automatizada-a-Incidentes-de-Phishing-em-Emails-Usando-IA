import pandas as pd
import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.core.constants import MODEL_PATH
from src.core.utils import (
    verificar_arquivos_essenciais, 
    logger,
    decodificar_corpo_email,
    limpar_html
)
from src.auth.gmail_auth import criar_servico
from src.core.detector import DetectorPhishing
from src.core.responder import RespondedorIncidentes
from src.auth.gmail_auth import criar_servico

def listar_emails(service, num_emails: int = 10) -> pd.DataFrame:
    """Busca e-mails não lidos da conta Gmail."""
    try:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread"
        ).execute()
        
        messages = results.get('messages', [])
        emails = []
        
        for message in messages[:num_emails]:
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            subject = headers.get('Subject', 'Sem assunto')
            
            # Processa o corpo do e-mail
            if 'parts' in msg['payload']:
                body = next(
                    (part['body']['data'] for part in msg['payload']['parts'] 
                     if part['mimeType'] == 'text/plain'),
                    None
                )
                body = decodificar_corpo_email({'data': body}) if body else 'Corpo não disponível'
            else:
                body = decodificar_corpo_email(msg['payload']['body'])
            
            emails.append({
                'assunto': subject,
                'conteudo': limpar_html(body),
                'is_phishing': None
            })
        
        return pd.DataFrame(emails)
    
    except Exception as error:
        logger.error(f'Erro ao listar e-mails: {error}')
        return pd.DataFrame()
    
def main():
    try:
        usuario = input("Digite seu nome de usuário: ").strip() or "default"
        
        logger.info("Iniciando autenticação com Gmail API...")
        service = criar_servico(usuario=usuario)
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

    try:
        verificar_arquivos_essenciais()
        logger.info("Iniciando autenticação com Gmail API...")
        
        service = criar_servico()
        logger.info("Buscando e-mails da conta do Gmail...")
        
        emails_df = listar_emails(service, num_emails=10)
        
        if not emails_df.empty:
            logger.info(f"{len(emails_df)} e-mails encontrados para análise")
            
            detector = DetectorPhishing()
            previsoes = detector.prever(emails_df)
            
            respondedor = RespondedorIncidentes()
            respondedor.tomar_acao(emails_df, previsoes)
        else:
            logger.info("Nenhum e-mail encontrado para análise.")
    
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main()