# ✅ النسخة النهائية المعدلة من chat10_final.py بعد تصحيح المشاكل المطلوبة

import os
import io
from fpdf import FPDF
import streamlit as st
from modules.memory_manager import SessionMemory, save_questions_to_file, load_questions_from_file
from modules.file_loader import load_and_split_documents
from modules.prompt_templates import build_prompt
from modules.llm_chain_client import ask_llm
from modules.chroma_manager import build_or_load_chroma_for_material, build_or_load_chroma_for_upload

# --- PDF Helper Function ---
def questions_to_pdf(questions_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for q in questions_list:
        for line in q.split('\n'):
            pdf.cell(0, 10, line, ln=True)
        pdf.ln(5)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_bytes)

# ---- Folder Reading ----
def get_grades(base_folder="pdf"):
    if not os.path.exists(base_folder):
        return []
    return sorted([grade for grade in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, grade))])

def get_subjects_for_grade(grade_folder):
    full_path = os.path.join("pdf", grade_folder)
    if not os.path.exists(full_path):
        return []
    subjects = []
    for file in os.listdir(full_path):
        if file.lower().endswith((".pdf", ".docx", ".txt")):
            subject_name = os.path.splitext(file)[0]
            subjects.append(subject_name)
    return subjects

def get_pdf_path(grade, subject):
    for ext in [".pdf", ".docx", ".txt"]:
        full_path = os.path.join("pdf", grade, subject + ext)
        if os.path.exists(full_path):
            return full_path
    return None

# ---- Navigation functions ----
def go_to_stored_materials():
    st.session_state.selection = "Stored Materials"
    st.session_state.page = "stored"

def go_to_upload_material():
    st.session_state.selection = "Upload Material"
    st.session_state.page = "upload"

def go_home():
    st.session_state.page = "home"
    st.session_state.selection = None
    st.session_state.uploaded_file = None

# ---- Main app logic ----
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Student", "Admin"])

    if page == "Admin":
        st.title("Admin: Upload School Material")
        grades = get_grades()
        grade = st.selectbox("Select or add a grade", grades + ["Add new grade"])
        if grade == "Add new grade":
            grade = st.text_input("Enter new grade name")
        subjects = get_subjects_for_grade(grade) if grade and grade != "Add new grade" else []
        subject = st.selectbox("Select or add a subject", subjects + ["Add new subject"])
        if subject == "Add new subject":
            subject = st.text_input("Enter new subject name")
        uploaded_file = st.file_uploader("Upload material (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
        if uploaded_file and grade and subject:
            ext = os.path.splitext(uploaded_file.name)[1]
            save_path = os.path.join("pdf", grade, subject + ext)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded {uploaded_file.name} to {grade}/{subject}")

    else:
        if "memory" not in st.session_state:
            st.session_state.memory = SessionMemory()
        memory = st.session_state.memory

        if "page" not in st.session_state:
            st.session_state.page = "home"
        if "selection" not in st.session_state:
            st.session_state.selection = None
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None

        st.sidebar.title("🎓 Student Login")
        student_id = st.sidebar.text_input("Enter your Student ID or Name:")
        if not student_id:
            st.warning("Please enter your Student ID in the sidebar to begin.")
            st.stop()

        if st.session_state.page == "home":
            st.title("📚 Educational Chatbot by ENG:Dai Elsayed")
            st.write("Choose how you want to proceed:")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Study materials"):
                    go_to_stored_materials()
            with col2:
                if st.button("📤 Upload PDF"):
                    go_to_upload_material()

        elif st.session_state.page == "stored":
            st.title("📂 Stored Materials")

            if st.button("⬅️ Back to Home", key="back1"):
                go_home()

            grades = get_grades()
            selected_grade = st.selectbox("Choose Academic Year", options=["Select a year"] + grades)

            if selected_grade != "Select a year":
                subjects = get_subjects_for_grade(selected_grade)
                selected_subject = st.selectbox("Choose Subject", options=["Select a subject"] + subjects)

                if selected_subject != "Select a subject":
                    question_types = ["MCQ", "True/False", "Short Answer", "Essay"]
                    selected_question_type = st.selectbox("Question Type", question_types)
                    num_questions = st.slider("Number of Questions", 1, 10, 5)
                    scope = st.radio("Choose Scope", ["General", "Topic"])
                    topic = st.text_input("Enter Topic") if scope == "Topic" else None

                    if "all_results" not in st.session_state:
                        st.session_state.all_results = []
                    if st.button("Generate Questions"):
                        persist_directory = build_or_load_chroma_for_material(selected_grade, selected_subject)

                        prompt_data = {
                            "subject": selected_subject,
                            "question_type": selected_question_type,
                            "scope": scope,
                            "topic": topic,
                            "school_year": selected_grade
                        }
                        prompt = build_prompt(**prompt_data, num_questions=num_questions, persist_directory=persist_directory)
                        result = ask_llm(prompt)
                        memory.save_context(prompt_data, [result])
                        st.session_state.all_results.append(result)
                        save_questions_to_file(student_id, [result])

                    if st.session_state.all_results:
                        st.markdown("### 🧠 Generated Questions")
                        for res in st.session_state.all_results:
                            st.write(res)
                            st.markdown("---")

                        if st.button("🔁 More Questions on Same Topic"):
                            if memory.has_context():
                                last_prompt_data = memory.get_last_prompt()
                                persist_directory = build_or_load_chroma_for_material(
                                    last_prompt_data["school_year"], last_prompt_data["subject"]
                                )
                                prompt = build_prompt(
                                    **last_prompt_data,
                                    num_questions=3,
                                    persist_directory=persist_directory
                                )
                                result = ask_llm(prompt)
                                memory.save_context(last_prompt_data, [result])
                                st.session_state.all_results.append(result)
                                save_questions_to_file(student_id, [result])

                        if st.button("Download"):
                            questions_text = "\n\n---\n\n".join(st.session_state.all_results)
                            st.download_button("Download Questions as TXT", data=questions_text, file_name="generated_questions.txt", mime="text/plain")
                            pdf_file = questions_to_pdf(st.session_state.all_results)
                            st.download_button("Download Questions as PDF", data=pdf_file, file_name="generated_questions.pdf", mime="application/pdf")

                        if st.button("📂 Old Questions"):
                            old = load_questions_from_file(student_id)
                            if old:
                                st.markdown("### 📜 Your Previously Generated Questions")
                                for q in old:
                                    st.write(q)
                                    st.markdown("---")
                            else:
                                st.info("No previous questions saved for this ID.")

        elif st.session_state.page == "upload":
            st.title("📤 Upload New Material")

            if st.button("⬅️ Back to Home", key="back2"):
                go_home()

            uploaded_file = st.file_uploader("Upload a textbook (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
            if uploaded_file:
                path = os.path.join("temp_upload", uploaded_file.name)
                os.makedirs("temp_upload", exist_ok=True)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                subject_name = os.path.splitext(uploaded_file.name)[0]
                persist_directory = build_or_load_chroma_for_upload(student_id, path)

                st.success("Upload successful. Now you can chat and generate questions.")

                question_types = ["MCQ", "True/False", "Short Answer", "Essay"]
                selected_question_type = st.selectbox("Question Type", question_types)
                num_questions = st.slider("Number of Questions", 1, 10, 5)
                scope = st.radio("Choose Scope", ["General", "Topic"])
                topic = st.text_input("Enter Topic") if scope == "Topic" else None

                if "upload_results" not in st.session_state:
                    st.session_state.upload_results = []
                if st.button("Generate Questions", key="upload_generate"):
                    prompt_data = {
                        "subject": subject_name,
                        "question_type": selected_question_type,
                        "scope": scope,
                        "topic": topic,
                        "school_year": "Uploaded Material"
                    }
                    prompt = build_prompt(**prompt_data, num_questions=num_questions, persist_directory=persist_directory)
                    result = ask_llm(prompt)
                    memory.save_context(prompt_data, [result])
                    st.session_state.upload_results.append(result)
                    save_questions_to_file(student_id, [result])

                if st.session_state.upload_results:
                    st.markdown("### 🧠 Generated Questions")
                    for res in st.session_state.upload_results:
                        st.write(res)
                        st.markdown("---")

                    if st.button("🔁 More Questions on Same Topic", key="upload_more"):
                        if memory.has_context():
                            last_prompt_data = memory.get_last_prompt()
                            persist_directory = build_or_load_chroma_for_upload(student_id, path)
                            prompt = build_prompt(
                                **last_prompt_data,
                                num_questions=3,
                                persist_directory=persist_directory
                            )
                            result = ask_llm(prompt)
                            memory.save_context(last_prompt_data, [result])
                            st.session_state.upload_results.append(result)
                            save_questions_to_file(student_id, [result])

                    if st.button("Download"):
                        questions_text = "\n\n---\n\n".join(st.session_state.upload_results)
                        st.download_button("Download Questions as TXT", data=questions_text, file_name="generated_questions.txt", mime="text/plain")
                        pdf_file = questions_to_pdf(st.session_state.upload_results)
                        st.download_button("Download Questions as PDF", data=pdf_file, file_name="generated_questions.pdf", mime="application/pdf")

                    if st.button("📂 Old Questions"):
                        old = load_questions_from_file(student_id)
                        if old:
                            st.markdown("### 📜 Your Previously Generated Questions")
                            for q in old:
                                st.write(q)
                                st.markdown("---")
                        else:
                            st.info("No previous questions saved for this ID.")

if __name__ == "__main__":
    main()
