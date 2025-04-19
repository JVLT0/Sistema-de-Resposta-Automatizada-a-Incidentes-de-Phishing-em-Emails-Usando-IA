# 🛡️ Detector de Phishing em E-mails com IA
Um projeto acadêmico que utiliza BERT (Transformers) para identificar e-mails de phishing em contas do Gmail, com resposta automatizada a incidentes.

## 🛠️ Pré-requisitos
- Python 3.8+
- Conta no Google Cloud (para API Gmail)
- pip instalado

## 🚀 Como Executar
### **1. Clone o Repositório**
``` bash
git clone https://github.com/JVLT0/Sistema-de-Resposta-Automatizada-a-Incidentes-de-Phishing-em-Emails-Usando-IA
```
### **2. Configure a API Gmail**
#### 1. Criar um Projeto no Google Cloud
- Acessar [Google Cloud Console](https://console.cloud.google.com/)
- Criar um novo projeto (ex.: Phishing-Detector-Academico).

#### 2. Ativar a Gmail API
- Na seção "APIs e Serviços" > "Biblioteca", buscar por "Gmail API" e ativá-la.

#### 3. Criar Credenciais OAuth
- Ir em "APIs e Serviços" > "Credenciais" > "Criar Credenciais" > "ID do cliente OAuth".
- Selecionar Tipo de Aplicativo: "Aplicativo para Computador".
- Fazer download do client_secret.json e colocar na pasta config/ do projeto.
``` bash
phishing-detector/config/client_secret.json
```

#### 4. Adicionar-se como Usuário de Teste
- Em "Tela de Consentimento OAuth", adicionar o e-mail dela em "Usuários de Teste".
       
#### 5. Instale as Dependências
```
pip install -r data/requirements.txt
```
#### 6. Execute o Sistema
```
python -m src.main
```
- Na primeira execução, um navegador abrirá para autorizar o acesso ao Gmail.

## 📂 Estrutura do Projeto
```
Phishing_Detector/
├── config/               # Credenciais da API
│   └── client_secret.json
├── data/                 # Datasets e requirements
│   ├── dataset_emails.csv
│   └── requirements.txt
├── src/                  # Código-fonte
│   ├── auth/             # Autenticação Gmail
│   ├── core/             # Lógica principal
│   ├── training/         # Modelo BERT
│   └── main.py           # Ponto de entrada
└── models/               # Modelos treinados (gerado automaticamente)
```

## 🔍 Funcionalidades
- ✅ Detecção Automática: Classifica e-mails como "phishing" ou "legítimos" usando BERT.
- ✅ Resposta a Incidentes: Ações automáticas para e-mails maliciosos.
- ✅ Multi-usuário: Configuração independente para cada usuário.

## **⚠️ Importante!**
- **Nunca compartilhe client_secret.json ou token.json.**
- **Para uso acadêmico, limite-se a 100 autenticações/dia (cota gratuita da API).**

## 📜 Licença
- Este projeto é para fins acadêmicos. Desenvolvido como parte da disciplina de Linguagens Formais e Autômatos.

- 👨‍💻 Autor: João Vitor Leal Targino | Luis Gustavo de Carvalho Briedis
- 📧 Contato: joaovitor.lealtargino@outlook.com

### 🔎 Dúvidas? Consulte a documentação da [Gmail API](https://developers.google.com/gmail/api "Requer login no Google").
