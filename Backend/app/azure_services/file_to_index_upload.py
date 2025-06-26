import json
from ..config import Config
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType
)
from azure.core.credentials import AzureKeyCredential

endpoint = Config.AZURE_SEARCH_ENDPOINT
admin_key = Config.AZURE_SEARCH_KEY
index_name = "html-css-storage-index"

    
def upload_documents(website_name , website_id):


    
    search_client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(admin_key)
    )


    with open("html_css_cache/Freshgo_html.json") as f1, open("html_css_cache/Freshgo_css.json") as f2:
        html = json.load(f1)["html"]
        css = json.load(f2)["css"]

    doc = {
        "id": "freshgo",
        "store_name": "Freshgo",
        "html": html,
        "css": css
    }

    result = search_client.upload_documents(documents=[doc])

    with open("freshgo_combined.json", "w") as f:
        json.dump(doc, f, indent=2)

