import os
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from modules.file_loader import load_and_split_documents

def build_chroma_index(chunks, persist_directory="temp_chroma"):
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print(f"✅ Chroma already exists at: {persist_directory}")
        return

    print(f"⚙️ Building Chroma at: {persist_directory}")
    os.makedirs(persist_directory, exist_ok=True)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_texts(chunks, embedding=embedding_model, persist_directory=persist_directory)
    vectorstore.persist()

def load_chroma_index(persist_directory="temp_chroma"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=persist_directory, embedding_function=embedding_model)

def retrieve_relevant_chunks(query, persist_directory="temp_chroma", k=5):
    vectorstore = load_chroma_index(persist_directory)
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join([res.page_content for res in results])

def build_all_chroma_indexes(pdf_root="pdf", chroma_root="chroma"):
    for grade in os.listdir(pdf_root):
        grade_path = os.path.join(pdf_root, grade)
        if not os.path.isdir(grade_path):
            continue

        for file in os.listdir(grade_path):
            if file.lower().endswith((".pdf", ".docx", ".txt")):
                subject = os.path.splitext(file)[0]
                source_path = os.path.join(grade_path, file)
                chroma_path = os.path.join(chroma_root, grade, subject)

                if not os.path.exists(chroma_path) or not os.listdir(chroma_path):
                    print(f"⏳ Building: {grade}/{subject}")
                    chunks = load_and_split_documents([source_path])
                    build_chroma_index(chunks, persist_directory=chroma_path)
                else:
                    print(f"✅ Already exists: {grade}/{subject}")
