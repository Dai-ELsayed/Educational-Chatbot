def get_formatting_by_type(qtype):
    qtype = qtype.lower()
    if qtype == "mcq":
        return """
Format:
Number each question like this:
Q1: <Question text>
Options:
A. <Option 1>
B. <Option 2>
C. <Option 3>
D. <Option 4>
Answer: <Correct option letter>

- Each question should be on its own line.
- Each option should be on its own line, labeled A to D.
- The answer should be on a separate line.

Example:
Q1: What is the capital of France?  
A. Berlin  
B. Paris  
C. Madrid  
D. Rome  
Answer: B
"""

    elif qtype == "true/false":
        return """
Format:
Q1: <True/False question>
Answer: <True or False>

Example:
Q1: The Earth is the third planet from the Sun.  
Answer: True
"""

    elif qtype == "short answer":
        return """
Format:
Q1: <Short answer question>
Answer: <One-sentence answer>

Example:
Q1: What is the largest planet in our solar system?  
Answer: Jupiter
"""

    elif qtype == "essay":
        return """
Format:
Q1: <Essay-style question>
Answer: <Answer in 2–3 paragraphs>

Example:
Q1: Explain the process of photosynthesis.  
Answer: Photosynthesis is the process by which plants convert sunlight into energy. ...
"""

    else:
        return """
Format:
Q1: <Question>
Answer: <Answer>
"""


from modules.vector_store import retrieve_relevant_chunks
from modules.prompt_templates import get_formatting_by_type

def build_prompt(
    subject,
    question_type,
    scope,
    topic=None,
    text=None,
    school_year="Grade 5",
    num_questions=5,
    persist_directory=None  
):
    if scope == "topic" and topic:
        text_scope_instruction = f"Focus only on the topic: {topic}."
        if not text and persist_directory:
            text = retrieve_relevant_chunks(topic, persist_directory=persist_directory)
    else:
        text_scope_instruction = "Use the general content."
        if not text and persist_directory:
            text = retrieve_relevant_chunks(subject, persist_directory=persist_directory)

    formatting = get_formatting_by_type(question_type)

    prompt = f"""
You are a smart educational assistant.
Based on the following {subject} textbook content for {school_year}, generate {num_questions} high-quality {question_type} questions to help students understand the material.
{text_scope_instruction}

Text:
\"\"\"{text}\"\"\"

{formatting}
"""
    return prompt.strip()

