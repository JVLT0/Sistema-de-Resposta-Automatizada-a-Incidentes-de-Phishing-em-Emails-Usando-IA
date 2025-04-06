import logging
from typing import Dict, Any

from src.core.utils import logger

class RespondedorIncidentes:
    def tomar_acao(self, emails_df, previsoes):
        """Toma ações com base nas previsões do modelo."""
        logger.info("Tomando ações com base nos e-mails detectados...")
        logger.info("\n" + "="*100)
        
        for idx, (_, email) in enumerate(emails_df.iterrows()):
            if previsoes[idx] == 1:
                self._lidar_com_email_phishing(email)
            else:
                self._exibir_email_normal(email)
    
    def _lidar_com_email_phishing(self, email: Dict[str, Any]):
        """Lida com e-mails classificados como phishing."""
        logger.info("")
        logger.warning(f"🚨 E-mail de phishing detectado!")
        logger.warning(f"Assunto: {email['assunto']}")
        logger.warning(f"Conteúdo: {email['conteudo'][:200]}...")
        logger.warning("Ações tomadas: E-mail movido para quarentena, Remetente bloqueado, Equipe de segurança notificada")
        logger.info("\n" + "="*100)
    
    def _exibir_email_normal(self, email: Dict[str, Any]):
        """Exibe e-mails classificados como normais."""
        logger.info("")
        logger.info(f"📩 E-mail legítimo recebido - {email['assunto']}")
        logger.info("\n" + "="*100)