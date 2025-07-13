import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopos de acesso
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_gmail(to_email, subject, message_text, html_content=None):
    creds = None

    # Carrega o token de autenticação se existir
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se o token não for válido, solicita login via navegador
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Constrói o serviço Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Cria e-mail com suporte a texto simples e HTML
    message = MIMEMultipart('alternative')
    message['to'] = to_email
    message['subject'] = subject

    part1 = MIMEText(message_text, 'plain')
    message.attach(part1)

    if html_content:
        part2 = MIMEText(html_content, 'html')
        message.attach(part2)

    # Codifica e envia o e-mail
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}

    sent_message = service.users().messages().send(userId='me', body=body).execute()
    print(f"Mensagem enviada para {to_email}, ID: {sent_message['id']}")
