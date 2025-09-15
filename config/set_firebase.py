import os

firebase_project_settings = {
  "type": "service_account",
  "project_id": "chatbot-test-42baf",
  "private_key_id": os.environ["private_key_id"],
  "private_key": os.environ["private_key"].replace(r'\n', '\n'),
  "client_email": os.environ["client_email"],
  "client_id": os.environ["client_id"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ["client_x509_cert_url"],
  "universe_domain": "googleapis.com"
}