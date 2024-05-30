import ee
import json
import streamlit as st
from google.oauth2 import service_account
from ee import oauth

def ee_initialize(force_use_service_account=False):
    """Initialize Google Earth Engine using service account credentials."""

    if force_use_service_account or "json_data" in st.secrets:
        # Retrieve the JSON credentials from Streamlit secrets
        json_credentials = st.secrets["json_data"]

        # Parse the JSON credentials
        credentials_dict = json.loads(json_credentials)

        # Ensure 'client_email' is present in the credentials
        if 'client_email' not in credentials_dict:
            raise ValueError("Service account info is missing 'client_email' field.")

        # Add scopes to the credentials
        scopes = ['https://www.googleapis.com/auth/earthengine',
                  'https://www.googleapis.com/auth/devstorage.read_write']
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict, scopes=oauth.SCOPES
        )
        ee.Initialize(credentials)
    else:
        # Initialize with default credentials
        ee.Initialize()

# Usage example (where needed in your code)
ee_initialize(force_use_service_account=True)