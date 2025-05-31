import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(doc_paths, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []

    for path in doc_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".docx":
            loader = Docx2txtLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        else:
            st.warning(f"Unsupported file type: {ext}")
            continue


        docs = loader.load()
        chunks = splitter.split_documents(docs)
        all_chunks.extend([chunk.page_content for chunk in chunks])
        # all_chunks.extend(chunks)  # without .page_content


    return all_chunks
