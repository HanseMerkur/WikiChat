from langchain.document_loaders.base import BaseLoader
from langchain_community.document_loaders.confluence import ConfluenceLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
