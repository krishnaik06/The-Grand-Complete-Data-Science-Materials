from pydantic_settings import BaseSettings, SettingsConfigDict
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

import json
from typing import List
from pydantic import AnyHttpUrl
from cryptography.fernet import Fernet

class Settings(BaseSettings):

    # API Version
    API_V1_STR: str = "/api/v1"

    #region Azure Key Vault config - Uncomment this region if you want to configure Azure Key Vault
    # # Azure Key Vault config
    # # Generate and Store fernet_key in environment variable or store in private place
    # fernet_key = Fernet.generate_key()
    # fernet = Fernet(fernet_key)

    # KEYVAULT_TENANT_ID: str = "<GUID>"
    # KEYVAULT_CLIENT_ID: str = "<GUID>"

    # # Generate KEYVAULT_CLIENT_SECRET with fernet_key stored in environment variable or store in private place, fernet.encrypt("Azure client secret")
    # KEYVAULT_CLIENT_SECRET: str = b'gAAAAABk......'
    # KEYVAULT_URI: str = "https://<key_vault_name>.vault.azure.net/"

    # #Connect to Azure Key Vault
    # _credential = ClientSecretCredential(
    #     tenant_id=KEYVAULT_TENANT_ID,
    #     client_id=KEYVAULT_CLIENT_ID,
    #     client_secret=fernet.decrypt(KEYVAULT_CLIENT_SECRET)
    # )

    # # Get secret value from Azure Key Vault
    # secret_client = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
    # secret_value = secret_client.get_secret("<secret_name>").value
    #endregion

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database Connection strings
    # Change below connection string as per requirement
    CONNECTION_STRINGS:  str  = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=.\SQLEXPRESS;DATABASE=MusaddiqueHussainLabs;Trusted_Connection=yes;TrustServerCertificate=yes'
    ISSUER: str = 'http://localhost:8080'

    # JWT Config
    JWT_KEY: str = 'ee8b0035a3ea72d26ba26806e576c9bb961559b66cc3432f80ce41a88f259155'
    TID: str = '3c55a074-b53c-43f6-8feb-480e8c35ae2b'

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "9a9812b05324b30e41f7920b6e998b81f8e772f692478df96809549e77308dd3"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()