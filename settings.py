import os

from langchain_openai import ChatOpenAI

os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_ENDPOINT"] = os.getenv(
    "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
)
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

OPENAI_COMPAT_API_KEY = os.getenv("OPENAI_COMPAT_API_KEY")
if OPENAI_COMPAT_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_COMPAT_API_KEY

OPENAI_COMPAT_BASE_URL = os.getenv("OPENAI_COMPAT_BASE_URL", "https://api.openai.com/v1")
os.environ["OPENAI_BASE_URL"] = OPENAI_COMPAT_BASE_URL

CHROMA_HOST = os.getenv("CHROMA_HOST", "api.trychroma.com")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
CHROMA_TOKEN = os.getenv("CHROMA_TOKEN")

MODELS = {
    "gpt-3.5-turbo": ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=OPENAI_COMPAT_API_KEY,
        base_url=OPENAI_COMPAT_BASE_URL,
    ),
    "gpt-4o-mini": ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_COMPAT_API_KEY,
        base_url=OPENAI_COMPAT_BASE_URL,
    ),
    "gpt-4o": ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        api_key=OPENAI_COMPAT_API_KEY,
        base_url=OPENAI_COMPAT_BASE_URL,
    ),
    "o3-mini": ChatOpenAI(
        model="o3-mini",
        api_key=OPENAI_COMPAT_API_KEY,
        base_url=OPENAI_COMPAT_BASE_URL,
    ),
}
