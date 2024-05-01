from langchain.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

SUMMARY_PROMPT_TEMPLATE_DE = """
Fasse die Inhalte des bereitgestellten Dokuments zusammen und benutze dabei wichtige Schlüsselwörter:
        
---
{doc}
---
        
Assistant:
"""

SUMMARY_PROMPT_TEMPLATE_EN = """
Summarize the contents of the provided document, including important key words:
        
---
{doc}
---
        
Assistant:
"""


def load_docs(loader: BaseLoader):
    return loader.load()


def split_documents(
    text_splitter: RecursiveCharacterTextSplitter, documents: list[Document]
):
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def create_embeddings(embeddings: Embeddings, chunks):
    embeddings.embed_documents(texts=chunks)
