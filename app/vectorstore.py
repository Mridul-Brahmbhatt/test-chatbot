from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import HF_EMBED_MODEL

# Shared embedding model
embedding_model = HuggingFaceEmbeddings(model_name=HF_EMBED_MODEL)


def get_retriever(persist_dir: str):
    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    return db.as_retriever(search_kwargs={"k": 4})


# Two retrievers
nec_retriever = get_retriever("chroma_nec")
wattmonk_retriever = get_retriever("chroma_wattmonk")