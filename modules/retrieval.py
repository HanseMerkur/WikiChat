from typing import List
from langchain_core.documents import Document

BASE_SYSTEM_MESSAGE_DE = """Du bist ein hilfreicher Assistent, der Fragen von Benutzern beantwortet.
Dabei benutzt du den bereitgestellten Kontext.
"""

PROMPT_TEMPLATE_DE = """Nutze den nachfolgend bereitgestellten Kontext, um die Frage am Ende zu beantworten. 
Wenn du die Antwort nicht kennst, sage einfach, dass du es nicht weißt.

Kontext:

{context}

Frage: {question}

Detaillierte, eigenständig und verständlich formulierte Antwort:
"""


def format_docs(docs: List[Document]):
    """
    Formats a list of Documents by concatinating thei content into a single string
    and separating each piece of content with new lines and triple dash.
    """
    return "\n\n---\n\n".join([doc.page_content for doc in docs])
