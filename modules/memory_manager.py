import os
import json
import time

class SessionMemory:
    def __init__(self):
        self.last_prompt_data = None
        self.last_generated_questions = []

    def save_context(self, prompt_data, questions):
        self.last_prompt_data = prompt_data
        self.last_generated_questions = questions

    def get_last_prompt(self):
        return self.last_prompt_data

    def has_context(self):
        return self.last_prompt_data is not None


def save_questions_to_file(student_id, new_questions):
    import os
    import json

    os.makedirs("saved_questions", exist_ok=True)
    path = os.path.join("saved_questions", f"{student_id}.json")

    # Load existing questions
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    # Save as simple list of strings
    updated = existing + new_questions
    with open(path, "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)



def load_questions_from_file(student_id):
    path = os.path.join("saved_questions", f"{student_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
