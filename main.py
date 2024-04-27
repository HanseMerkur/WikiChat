import os

import chromadb
import ollama
from chromadb.config import Settings
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock
from langchain_chroma import Chroma
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from modules.retrieval import PROMPT_TEMPLATE_DE, format_docs

# current_dir = os.path.dirname(os.path.abspath(__file__))
# DOCU_PATH = os.path.join(current_dir, "data/docu")

# Confluence Wiki stuff
CONFLUENCE_PAT = os.getenv("CONFLUENCE_PAT")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

CHUNK_SIZE = 1000

# ChromaDB stuff
COLLECTION_NAME = f"{CHUNK_SIZE}_{CONFLUENCE_SPACE_KEY}"

# AWS stuff
CREDENTIALS_PROFILE_NAME = os.getenv("AWS_CREDENTIALS_PROFILE_NAME")
REGION_NAME = os.getenv("AWS_REGION_NAME", "eu-central-1")
AWS_LANGUAGE_MODEL_ID = os.getenv(
    "AWS_LANGUAGE_MODEL_ID", "amazon.titan-text-express-v1"
)
AWS_EMBEDDING_MODEL_ID = os.getenv(
    "AWS_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1"
)
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL_ID", "mxbai-embed-large")
OLLAMA_LANGUAGE_MODEL = os.getenv("OLLAMA_LANGUAGE_MODEL_ID", "mistral:7b")


def main(llm: BaseChatModel, embeddings: Embeddings, db_client: chromadb.HttpClient):

    db = Chroma(
        client=db_client, collection_name=COLLECTION_NAME, embedding_function=embeddings
    )
    question = input("Stelle eine Frage: ")

    # retrieve relevant docs/chunks
    retriever = db.as_retriever(search_kwargs={"k": 2})
    relevant_docs = retriever.get_relevant_documents(query=question)

    # print relevant docs content
    for doc in relevant_docs:
        print("\n---\n" + doc.page_content + "\n---\n")

    context_text = format_docs(relevant_docs)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_DE)

    chain = prompt | llm | StrOutputParser()
    resp = chain.invoke({"context": context_text, "question": question})
    print(resp)


if __name__ == "__main__":

    def initialize_ollama_chat_model(model_name: str) -> ChatOllama:
        return ChatOllama(model=model_name, temperature=0)

    def initialize_ollama_embeddings_model(model_name: str) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=model_name)

    def initialize_bedrock_chat_model() -> ChatBedrock:
        return ChatBedrock(
            credentials_profile_name=CREDENTIALS_PROFILE_NAME,
            region_name=REGION_NAME,
            model_id=AWS_LANGUAGE_MODEL_ID,
            model_kwargs={"temperature": 0.0, "maxTokenCount": 1024},
        )

    def initialize_bedrock_embeddings_model() -> BedrockEmbeddings:
        return BedrockEmbeddings(
            credentials_profile_name=CREDENTIALS_PROFILE_NAME,
            region_name=REGION_NAME,
            model_id=AWS_EMBEDDING_MODEL_ID,
        )

    # Fetching the model details from the Ollama list method
    try:
        ollama_models = ollama.list()["models"]
    except Exception as e:
        ollama_models = []

    llm_options = {}
    menu_options_llms = []

    if ollama_models:
        for i, model in enumerate(ollama_models):
            model_id = model["model"]
            llm_options[str(i)] = (
                lambda model_id=model_id: initialize_ollama_chat_model(model_id)
            )
            menu_options_llms.append(f"{i} - ollama ({model_id}) \n")

    # Adding the Bedrock model as an additional option
    llm_options[str(len(ollama_models))] = initialize_bedrock_chat_model
    menu_options_llms.append(
        f"{len(ollama_models)} - Amazon Bedrock ({AWS_LANGUAGE_MODEL_ID}) \n"
    )

    chosen_option_llm = input(
        "Wähle ein Sprachmodell aus, das deine Anfragen beantworten wird. \n"
        + "".join(menu_options_llms)
        + "Gebe eine Nummer ein: "
    )

    chosen_chat_model = llm_options.get(chosen_option_llm, lambda: None)()
    if not chosen_chat_model:
        print("Ungültige Eingabe. Bitte starte das Programm neu.")
    else:
        print()
        embeddings_options = {
            "0": initialize_bedrock_embeddings_model,
            "1": lambda: initialize_ollama_embeddings_model(
                model_name="mxbai-embed-large"
            ),
            "2": lambda: initialize_ollama_embeddings_model(
                model_name="nomic-embed-text"
            ),
            "3": lambda: initialize_ollama_embeddings_model(model_name="all-minilm"),
        }

        chosen_option_embeddings_model = input(
            "Wähle das Modell für Embeddings aus, mit dem du deine Dokumente vektorisiert hast. \n"
            + f"0 - Amazon Bedrock ({AWS_EMBEDDING_MODEL_ID}) \n"
            + "1 - Ollama Embedding Model (mxbai-embed-large) \n"
            + "2 - Ollama Embedding Model (nomic-embed-text) \n"
            + "3 - Ollama Embedding Model (all-minilm) \n"
            + "Gebe eine Nummer ein: "
        )

        embeddings_function = embeddings_options.get(
            chosen_option_embeddings_model, lambda: None
        )()

        if embeddings_function is None:
            print("Ungültige Eingabe. Bitte starte das Programm neu.")
        else:
            chroma_settings = Settings(allow_reset=True)
            chroma_client = chromadb.HttpClient(settings=chroma_settings)

            main(
                llm=chosen_chat_model,
                embeddings=embeddings_function,
                db_client=chroma_client,
            )
