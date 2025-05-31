import os
from modules.vector_store import build_chroma_index, retrieve_relevant_chunks
from modules.file_loader import load_and_split_documents
from utils.hashing import get_unique_chroma_path

def build_or_load_chroma_for_material(grade, subject, pdf_root="pdf", chroma_root="chroma"):
    """
    Use for curriculum materials.
    """
    source_path = os.path.join(pdf_root, grade, subject + ".pdf")
    persist_directory = os.path.join(chroma_root, grade, subject)

    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        print(f"⏳ Building Chroma for: {grade}/{subject}")
        chunks = load_and_split_documents([source_path])
        build_chroma_index(chunks, persist_directory=persist_directory)
    else:
        print(f"✅ Chroma already exists for: {grade}/{subject}")

    return persist_directory


def build_or_load_chroma_for_upload(student_id, uploaded_file_path, chroma_root="chroma/uploads"):
    """
    Use for uploaded files by students.
    """
    unique_id = f"{student_id}_{os.path.basename(uploaded_file_path)}"
    persist_directory = get_unique_chroma_path(unique_id, chroma_root=chroma_root)

    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        print(f"⚙️ Building Chroma for upload: {uploaded_file_path}")
        chunks = load_and_split_documents([uploaded_file_path])
        build_chroma_index(chunks, persist_directory=persist_directory)
    else:
        print(f"✅ Chroma already exists for upload: {uploaded_file_path}")

    return persist_directory
