import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedding = HuggingFaceEmbeddings(model_name=HF_MODEL)


def process_pdf(paths, persist_dir, source_name):

    all_docs = []

    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")

        loader = PyPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    splits = splitter.split_documents(all_docs)

    for doc in splits:
        doc.metadata["source"] = source_name

    db = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_dir
    )

    db.persist()

    print(f"✅ {source_name} ingestion complete!")


if __name__ == "__main__":

    # NEC
    process_pdf(
        ["data/nec/414.pdf"],
        "chroma_nec",
        "NEC"
    )

    # Wattmonk
    process_pdf(
        [
            "data/wattmonk/Wattmonk (1) (1) (1).pdf",
            "data/wattmonk/Wattmonk Information (1).pdf"
        ],
        "chroma_wattmonk",
        "WATTMONK"
    )