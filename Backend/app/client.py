from openai import AzureOpenAI
from .config import Config

client = AzureOpenAI(
    api_key=Config.OPENAI_API_KEY,
    api_version="2025-01-01-preview",
    azure_endpoint="https://shoop-ma9lhvun-eastus2.openai.azure.com"
)
