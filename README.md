# Wiki Chat

RAG-based application for Q&A with data from your Confluence Wiki using LangChain, ChromaDB, AWS Bedrock or Ollama.

> :warning: The project is in a very early development stage. I would even call it as experimental, so don't rely on further development, support etc. However, we welcome contributions.

> :de: The code is written in english but the prompt templates are currently only available in german, as the app is initially designed to be used in a german company. Feel free to submit PRs for other languages.

## Installation and usage

Before you start, those requirements should be met:

- Python installed
- Docker and docker-compose installed
- access to either Amazon Bedrock or Ollama embeddings and language models
- You should have a Personal Access Token (PAT) for Confluence
- if you want to use Bedrock, configure the credentials as described [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)

### Step 1 - virtual env and requirements

Set up a virtual invironment and install requirements.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2 - Indexing

Indexing - loading your documents into a DB for later retrieval - is done by running one of the notebooks in the `notebooks` directory. There are multiple options available:

#### 1. Basic indexing

Here the most basic approach to indexing is implemented. We split the confluence documents recursively by characters, embed them and save them into a vector database for later retrieval. See notebook for more details.

Before you run the notebook, ensure that you environment is set up (see notebook) and that you have [ChromaDB](https://docs.trychroma.com/) up and running. To run an instance locally, use the `docker-compose.yaml` provided in the repo. Run it with:

```bash
docker-compose up -d vector-db
```

When run locally, Chroma will save it's data in the `data/chroma` directory.

#### 2. Multi-represenation indexing

This is a more advanced approach to indexing, which may be beneficial when you have access to fast LLM with a large context window. Here we retrieve full confluence documents using the embdedding of their summaries. For details, see notebook.

As in the previous option, set up your environment. Additionaly you'll need a local instance of redis DB up and running. To achieve this, run:

```bash
docker-compose up -d
```

### Step 2 - run the app

Execute `main.py` from command line. Before you do that, make sure that you modify the `CHUNK_SIZE` constant at the top of the script according to the size you have chosen in the previous step. When the script is executed, you will be prompted to select a language model. The options are partially based on the Ollama models you have downloaded, if there are any. The other option is Amazon Bedrock.

## Helpful resources

Here are some useful resources related to RAG, LLMs etc.:

### RAG in general

- [LangChain Hub (for prompt templates)](https://smith.langchain.com/hub)
- [Playlist "RAG from Scratch by LangChain"](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&si=0cMFgR5tLb6F5twH)
- [basic RAG tutorial by pixegami (youtube)](https://youtu.be/tcqEUSNCn8I?si=u510JlZE-7VfeSTG)
  - [github](https://github.com/pixegami/langchain-rag-tutorial/tree/main)

### from AWS

- [Amazon Bedrock Prompting Examples & Tools](https://github.com/aws-samples/amazon-bedrock-prompting)
- [RAG using LangChain with Amazon Bedrock Titan text, and embedding, using OpenSearch vector engine](https://github.com/aws-samples/rag-using-langchain-amazon-bedrock-and-opensearch)

### ChromaDB

- [AWS deployment](https://docs.trychroma.com/deployment#simple-aws-deployment)

## License

TODO
