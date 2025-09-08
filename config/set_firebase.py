import streamlit as st

firebase_project_settings = {
  "type": "service_account",
  "project_id": "chatbot-test-42baf",
  "private_key_id": st.secrets["firebase"]["private_key_id"],
  "private_key": st.secrets["firebase"]["private_key"],
  "client_email": st.secrets["firebase"]["client_email"],
  "client_id": st.secrets["firebase"]["client_id"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
  "universe_domain": "googleapis.com"
}