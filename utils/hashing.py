import os
import hashlib

def get_unique_chroma_path(source_id, chroma_root="chroma/uploads"):
    hash_id = hashlib.md5(source_id.encode()).hexdigest()
    return os.path.join(chroma_root, f"index_{hash_id}")
