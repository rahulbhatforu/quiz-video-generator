import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Quiz Video Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .question-card {
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []

if "quiz_title" not in st.session_state:
    st.session_state.quiz_title = ""

if "quiz_description" not in st.session_state:
    st.session_state.quiz_description = ""

# Set up data directory
DATA_DIR = Path("quiz_data")
DATA_DIR.mkdir(exist_ok=True)

def save_quiz():
    """Save quiz to JSON file"""
    if not st.session_state.quiz_title:
        st.error("Please enter a quiz title")
        return False
    
    if not st.session_state.questions:
        st.error("Please add at least one question")
        return False
    
    quiz_data = {
        "title": st.session_state.quiz_title,
        "description": st.session_state.quiz_description,
        "created_at": datetime.now().isoformat(),
        "questions": st.session_state.questions
    }
    
    filename = f"{st.session_state.quiz_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = DATA_DIR / filename
    
    with open(filepath, "w") as f:
        json.dump(quiz_data, f, indent=2)
    
    return True, filepath

def load_quizzes():
    """Load all saved quizzes"""
    quizzes = []
    if DATA_DIR.exists():
        for file in DATA_DIR.glob("*.json"):
            with open(file, "r") as f:
                quizzes.append({
                    "file": file.name,
                    "data": json.load(f)
                })
    return quizzes

def add_question(question_text, question_type, options=None, correct_answer=None, explanation=""):
    """Add a question to the quiz"""
    question = {
        "id": len(st.session_state.questions) + 1,
        "question": question_text,
        "type": question_type,
        "options": options or [],
        "correct_answer": correct_answer,
        "explanation": explanation
    }
    st.session_state.questions.append(question)

# Main title
st.markdown("# 🎯 Quiz Video Generator")
st.markdown("Create interactive quiz questions for your video content")

# Sidebar
with st.sidebar:
    st.markdown("## 📋 Navigation")
    page = st.radio("Select Page", ["Create Quiz", "View Quizzes", "About"])

# Main content
if page == "Create Quiz":
    st.markdown("## Create a New Quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.quiz_title = st.text_input(
            "Quiz Title",
            value=st.session_state.quiz_title,
            placeholder="e.g., Python Basics Quiz"
        )
    
    with col2:
        st.session_state.quiz_description = st.text_area(
            "Quiz Description",
            value=st.session_state.quiz_description,
            placeholder="Brief description of the quiz",
            height=100
        )
    
    st.markdown("---")
    st.markdown("## Add Questions")
    
    # Add question form
    with st.form("add_question_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            question_text = st.text_area(
                "Question Text",
                placeholder="Enter your question here",
                height=80
            )
        
        with col2:
            question_type = st.selectbox(
                "Question Type",
                ["Multiple Choice", "True/False", "Short Answer"]
            )
        
        if question_type == "Multiple Choice":
            st.markdown("### Answer Options")
            col1, col2 = st.columns(2)
            with col1:
                option1 = st.text_input("Option 1", key="opt1")
                option3 = st.text_input("Option 3", key="opt3")
            with col2:
                option2 = st.text_input("Option 2", key="opt2")
                option4 = st.text_input("Option 4", key="opt4")
            
            options = [opt for opt in [option1, option2, option3, option4] if opt]
            correct_option = st.selectbox("Correct Answer", options) if options else None
            
        elif question_type == "True/False":
            correct_option = st.selectbox("Correct Answer", ["True", "False"])
            options = ["True", "False"]
        
        else:  # Short Answer
            correct_option = st.text_input("Correct Answer")
            options = None
        
        explanation = st.text_area(
            "Explanation (Optional)",
            placeholder="Explain why this is the correct answer",
            height=60
        )
        
        submitted = st.form_submit_button("➕ Add Question", use_container_width=True)
        
        if submitted:
            if not question_text:
                st.error("Please enter a question")
            elif not correct_option:
                st.error("Please select or enter a correct answer")
            else:
                add_question(question_text, question_type, options, correct_option, explanation)
                st.success("Question added successfully! ✅")
    
    st.markdown("---")
    st.markdown("## Questions Preview")
    
    if st.session_state.questions:
        for idx, q in enumerate(st.session_state.questions, 1):
            with st.expander(f"Q{idx}: {q['question'][:50]}..."):
                st.markdown(f"**Type:** {q['type']}")
                if q['options']:
                    st.markdown("**Options:**")
                    for opt in q['options']:
                        st.markdown(f"- {opt}")
                st.markdown(f"**Correct Answer:** {q['correct_answer']}")
                if q['explanation']:
                    st.markdown(f"**Explanation:** {q['explanation']}")
                
                if st.button("❌ Remove Question", key=f"remove_{idx}"):
                    st.session_state.questions.pop(idx - 1)
                    st.rerun()
    else:
        st.info("No questions added yet. Start by adding a question above!")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Quiz", use_container_width=True):
            result = save_quiz()
            if isinstance(result, tuple):
                st.success(f"Quiz saved successfully! 📁\nFile: {result[1].name}")
                st.session_state.questions = []
                st.session_state.quiz_title = ""
                st.session_state.quiz_description = ""
    
    with col2:
        if st.button("🔄 Clear All", use_container_width=True):
            st.session_state.questions = []
            st.session_state.quiz_title = ""
            st.session_state.quiz_description = ""
            st.info("Quiz cleared!")

elif page == "View Quizzes":
    st.markdown("## 📚 Saved Quizzes")
    
    quizzes = load_quizzes()
    
    if quizzes:
        for quiz in quizzes:
            with st.expander(f"📖 {quiz['data']['title']}"):
                st.markdown(f"**Description:** {quiz['data']['description']}")
                st.markdown(f"**Created:** {quiz['data']['created_at']}")
                st.markdown(f"**Total Questions:** {len(quiz['data']['questions'])}")
                
                with st.expander("View Questions"):
                    for idx, q in enumerate(quiz['data']['questions'], 1):
                        st.markdown(f"**Q{idx}: {q['question']}**")
                        if q['options']:
                            for opt in q['options']:
                                st.markdown(f"  - {opt}")
                        st.markdown(f"✓ Answer: {q['correct_answer']}")
                        if q.get('explanation'):
                            st.markdown(f"💡 {q['explanation']}")
                        st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"📄 File: `{quiz['file']}`")
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{quiz['file']}"):
                        (DATA_DIR / quiz['file']).unlink()
                        st.success("Quiz deleted!")
                        st.rerun()
    else:
        st.info("No quizzes saved yet. Create one to get started!")

elif page == "About":
    st.markdown("## About Quiz Video Generator")
    
    st.markdown("""
    ### Welcome! 👋
    
    **Quiz Video Generator** is a tool designed to help you create interactive quizzes
    for your video content. With this interface, you can:
    
    ✨ **Features:**
    - ➕ Add questions of multiple types (Multiple Choice, True/False, Short Answer)
    - 📝 Provide explanations for each answer
    - 💾 Save quizzes as JSON files
    - 📚 View and manage your saved quizzes
    - 🎯 Organize questions with titles and descriptions
    
    ### How to Use:
    
    1. **Create Quiz:** Go to the "Create Quiz" tab
    2. **Enter Details:** Add a title and description for your quiz
    3. **Add Questions:** Use the form to add questions one by one
    4. **Preview:** Check your questions in the preview section
    5. **Save:** Save your quiz to generate a JSON file
    6. **Manage:** View, edit, or delete saved quizzes
    
    ### File Format:
    Quizzes are saved as JSON files with the following structure:
    ```json
    {
        "title": "Quiz Title",
        "description": "Quiz Description",
        "created_at": "ISO timestamp",
        "questions": [
            {
                "id": 1,
                "question": "Question text",
                "type": "Multiple Choice",
                "options": ["Option 1", "Option 2", ...],
                "correct_answer": "Option 1",
                "explanation": "Why this is correct"
            }
        ]
    }
    ```
    
    ---
    
    Made with ❤️ for educators and content creators
    """)

# Footer
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray;'>Quiz Video Generator © 2025 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True
)
