"""
Quiz Generator Pro - Advanced Streamlit Application
Bulk question import, video settings, and automatic video generation
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
import subprocess
import tempfile
from typing import List, Dict, Tuple
import time
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Quiz Generator Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE MANAGEMENT ====================
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'video_settings' not in st.session_state:
    st.session_state.video_settings = {
        'resolution': '1080p',
        'fps': 30,
        'duration_per_question': 10,
        'background_music': True,
        'subtitles': True,
        'transitions': 'fade',
        'text_font': 'Arial',
        'font_size': 24,
        'background_color': '#1a1a1a',
        'text_color': '#ffffff'
    }
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'current_job' not in st.session_state:
    st.session_state.current_job = None


# ==================== UTILITY FUNCTIONS ====================
def validate_questions(questions: List[Dict]) -> Tuple[bool, str]:
    """Validate question format and content"""
    if not questions:
        return False, "No questions provided"
    
    for idx, q in enumerate(questions, 1):
        if not q.get('question'):
            return False, f"Question {idx}: Missing question text"
        if not q.get('options') or len(q.get('options', [])) < 2:
            return False, f"Question {idx}: Need at least 2 options"
        if 'correct_answer' not in q:
            return False, f"Question {idx}: Missing correct answer"
        if q.get('correct_answer') not in q.get('options', []):
            return False, f"Question {idx}: Correct answer not in options"
    
    return True, "All questions validated successfully"


def parse_csv_questions(file_content: str) -> Tuple[List[Dict], str]:
    """Parse CSV file for questions"""
    try:
        df = pd.read_csv(BytesIO(file_content.encode()))
        required_cols = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            return [], f"Missing columns: {', '.join(missing)}"
        
        questions = []
        for idx, row in df.iterrows():
            questions.append({
                'question': row['question'],
                'options': [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
                'correct_answer': row['correct_answer'],
                'explanation': row.get('explanation', ''),
                'difficulty': row.get('difficulty', 'medium')
            })
        
        return questions, f"Successfully parsed {len(questions)} questions"
    except Exception as e:
        return [], f"Error parsing CSV: {str(e)}"


def parse_json_questions(file_content: str) -> Tuple[List[Dict], str]:
    """Parse JSON file for questions"""
    try:
        questions = json.loads(file_content)
        if not isinstance(questions, list):
            return [], "JSON must contain a list of questions"
        return questions, f"Successfully parsed {len(questions)} questions"
    except json.JSONDecodeError as e:
        return [], f"Invalid JSON format: {str(e)}"
    except Exception as e:
        return [], f"Error parsing JSON: {str(e)}"


def export_questions(questions: List[Dict], format_type: str) -> bytes:
    """Export questions in specified format"""
    if format_type == "csv":
        df = pd.DataFrame(questions)
        return df.to_csv(index=False).encode()
    elif format_type == "json":
        return json.dumps(questions, indent=2).encode()
    return b""


def generate_video_config(settings: Dict) -> Dict:
    """Generate video configuration from settings"""
    return {
        'video': {
            'resolution': settings['resolution'],
            'fps': settings['fps'],
            'codec': 'h264'
        },
        'timing': {
            'question_duration': settings['duration_per_question'],
            'answer_reveal_delay': 3,
            'transition_duration': 1
        },
        'styling': {
            'background_color': settings['background_color'],
            'text_color': settings['text_color'],
            'font_family': settings['text_font'],
            'font_size': settings['font_size'],
            'use_subtitles': settings['subtitles'],
            'transition_effect': settings['transitions']
        },
        'audio': {
            'background_music': settings['background_music'],
            'text_to_speech': True,
            'music_volume': 0.3
        }
    }


def generate_video(questions: List[Dict], settings: Dict, quiz_name: str) -> Tuple[bool, str]:
    """Simulate video generation process"""
    try:
        # Validate questions first
        is_valid, message = validate_questions(questions)
        if not is_valid:
            return False, message
        
        # Create video configuration
        video_config = generate_video_config(settings)
        
        # Simulate video generation with progress
        total_steps = len(questions) + 5
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for step in range(total_steps):
            progress_bar.progress((step + 1) / total_steps)
            
            if step < len(questions):
                status_text.text(f"Processing question {step + 1}/{len(questions)}")
            elif step == len(questions):
                status_text.text("Rendering video...")
            elif step == len(questions) + 1:
                status_text.text("Adding audio...")
            elif step == len(questions) + 2:
                status_text.text("Adding subtitles...")
            elif step == len(questions) + 3:
                status_text.text("Finalizing video...")
            else:
                status_text.text("Video generation complete!")
            
            time.sleep(0.5)
        
        # Record in history
        job_info = {
            'timestamp': datetime.now().isoformat(),
            'quiz_name': quiz_name,
            'question_count': len(questions),
            'settings': settings,
            'status': 'completed',
            'output_file': f"{quiz_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        }
        st.session_state.generation_history.append(job_info)
        
        return True, f"Video generated successfully: {job_info['output_file']}"
    
    except Exception as e:
        return False, f"Error generating video: {str(e)}"


def display_question_card(question: Dict, index: int):
    """Display a formatted question card"""
    with st.container():
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown(f"**#{index}**")
        with col2:
            st.write(f"**{question.get('question', 'N/A')}**")
        
        st.markdown("**Options:**")
        cols = st.columns(2)
        options = question.get('options', [])
        for i, option in enumerate(options):
            with cols[i % 2]:
                if option == question.get('correct_answer'):
                    st.success(f"✓ {option}")
                else:
                    st.write(f"○ {option}")
        
        if question.get('explanation'):
            st.info(f"📝 Explanation: {question['explanation']}")
        
        st.divider()


# ==================== MAIN APP ====================
def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("🎬 Quiz Generator Pro")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "📥 Import Questions", "⚙️ Video Settings", 
             "🎥 Generate Video", "📚 Question Manager", "📋 History"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.markdown("### Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions", len(st.session_state.questions))
        with col2:
            st.metric("Videos Generated", len(st.session_state.generation_history))
    
    # ==================== DASHBOARD PAGE ====================
    if page == "📊 Dashboard":
        st.title("📊 Quiz Generator Pro Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Questions", len(st.session_state.questions), delta="questions")
        with col2:
            st.metric("Videos Generated", len(st.session_state.generation_history), delta="videos")
        with col3:
            avg_duration = st.session_state.video_settings['duration_per_question']
            st.metric("Avg Duration/Q", f"{avg_duration}s", delta="per question")
        with col4:
            st.metric("Resolution", st.session_state.video_settings['resolution'], delta="current")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Recent Questions")
            if st.session_state.questions:
                recent = st.session_state.questions[-5:]
                for idx, q in enumerate(recent, 1):
                    st.write(f"{idx}. {q.get('question', 'N/A')[:60]}...")
            else:
                st.info("No questions imported yet")
        
        with col2:
            st.subheader("🎬 Recent Generations")
            if st.session_state.generation_history:
                recent_gen = st.session_state.generation_history[-5:]
                for gen in recent_gen:
                    timestamp = gen['timestamp'].split('T')[0]
                    st.write(f"📹 {gen['quiz_name']}")
                    st.caption(f"Questions: {gen['question_count']} | {timestamp}")
            else:
                st.info("No videos generated yet")
        
        st.divider()
        st.subheader("⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Import Questions", use_container_width=True):
                st.session_state.page = "📥 Import Questions"
                st.rerun()
        with col2:
            if st.button("⚙️ Configure Settings", use_container_width=True):
                st.session_state.page = "⚙️ Video Settings"
                st.rerun()
        with col3:
            if st.button("🎥 Generate Video", use_container_width=True):
                st.session_state.page = "🎥 Generate Video"
                st.rerun()
    
    # ==================== IMPORT QUESTIONS PAGE ====================
    elif page == "📥 Import Questions":
        st.title("📥 Import Questions")
        st.markdown("Import questions from CSV, JSON, or enter manually")
        
        import_method = st.radio(
            "Select import method:",
            ["📤 File Upload", "📝 Manual Entry", "📋 Paste Data"],
            horizontal=True
        )
        
        st.divider()
        
        if import_method == "📤 File Upload":
            st.subheader("Upload Question File")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**CSV Format Requirements:**")
                st.code("""question, option_a, option_b, option_c, option_d, correct_answer, explanation, difficulty""")
            
            with col2:
                st.markdown("**JSON Format:**")
                st.code("""[{
  "question": "...",
  "options": ["a", "b", "c", "d"],
  "correct_answer": "a",
  "explanation": "..."
}]""")
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["csv", "json"],
                help="Upload CSV or JSON file with questions"
            )
            
            if uploaded_file:
                file_content = uploaded_file.read().decode('utf-8')
                
                if uploaded_file.name.endswith('.csv'):
                    questions, message = parse_csv_questions(file_content)
                else:
                    questions, message = parse_json_questions(file_content)
                
                st.info(message)
                
                if questions:
                    st.success(f"✓ Ready to import {len(questions)} questions")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✓ Import Questions", use_container_width=True):
                            st.session_state.questions = questions
                            st.success(f"✓ Imported {len(questions)} questions successfully!")
                            time.sleep(1)
                            st.rerun()
                    
                    with col2:
                        if st.button("👁️ Preview", use_container_width=True):
                            st.session_state.show_preview = True
                    
                    if st.session_state.get('show_preview', False):
                        st.subheader("Preview")
                        for idx, q in enumerate(questions[:3], 1):
                            display_question_card(q, idx)
                        if len(questions) > 3:
                            st.info(f"... and {len(questions) - 3} more questions")
        
        elif import_method == "📝 Manual Entry":
            st.subheader("Add Questions Manually")
            
            with st.form("manual_question_form"):
                num_questions = st.number_input("Number of questions to add:", 1, 10, 1)
                
                questions_to_add = []
                for i in range(num_questions):
                    st.markdown(f"### Question {i + 1}")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        q_text = st.text_input(f"Question {i + 1}:", key=f"q_text_{i}")
                    with col2:
                        difficulty = st.selectbox(
                            "Difficulty:",
                            ["easy", "medium", "hard"],
                            key=f"difficulty_{i}"
                        )
                    
                    options = []
                    cols = st.columns(2)
                    for j in range(4):
                        with cols[j % 2]:
                            opt = st.text_input(
                                f"Option {chr(65 + j)}:",
                                key=f"option_{i}_{j}"
                            )
                            options.append(opt)
                    
                    correct = st.selectbox(
                        "Correct answer:",
                        options,
                        key=f"correct_{i}"
                    )
                    
                    explanation = st.text_area(
                        "Explanation (optional):",
                        key=f"explain_{i}"
                    )
                    
                    if q_text and all(options) and correct:
                        questions_to_add.append({
                            'question': q_text,
                            'options': options,
                            'correct_answer': correct,
                            'explanation': explanation,
                            'difficulty': difficulty
                        })
                    
                    st.divider()
                
                if st.form_submit_button("➕ Add Questions", use_container_width=True):
                    if questions_to_add:
                        st.session_state.questions.extend(questions_to_add)
                        st.success(f"✓ Added {len(questions_to_add)} questions!")
                        time.sleep(1)
                        st.rerun()
        
        elif import_method == "📋 Paste Data":
            st.subheader("Paste JSON or CSV Data")
            
            data_format = st.radio("Format:", ["JSON", "CSV"], horizontal=True)
            
            pasted_data = st.text_area("Paste your data here:", height=300)
            
            if st.button("📥 Parse and Import", use_container_width=True):
                if data_format == "JSON":
                    questions, message = parse_json_questions(pasted_data)
                else:
                    questions, message = parse_csv_questions(pasted_data)
                
                st.info(message)
                
                if questions:
                    st.session_state.questions = questions
                    st.success(f"✓ Imported {len(questions)} questions!")
                    time.sleep(1)
                    st.rerun()
    
    # ==================== VIDEO SETTINGS PAGE ====================
    elif page == "⚙️ Video Settings":
        st.title("⚙️ Video Settings Configuration")
        
        with st.form("video_settings_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎬 Video Properties")
                
                resolution = st.selectbox(
                    "Resolution:",
                    ["720p", "1080p", "1440p", "4K"],
                    index=1,
                    help="Output video resolution"
                )
                
                fps = st.slider(
                    "FPS:",
                    24, 60, 30,
                    help="Frames per second"
                )
                
                duration = st.slider(
                    "Duration per question (seconds):",
                    3, 30, 10,
                    help="How long each question is displayed"
                )
                
                transitions = st.selectbox(
                    "Transition Effect:",
                    ["fade", "slide", "zoom", "wipe", "dissolve"],
                    help="Transition between questions"
                )
            
            with col2:
                st.markdown("### 🎨 Styling")
                
                text_font = st.selectbox(
                    "Font Family:",
                    ["Arial", "Helvetica", "Times New Roman", "Courier", "Verdana"],
                    help="Text font for questions and options"
                )
                
                font_size = st.slider(
                    "Font Size:",
                    16, 48, 24,
                    help="Size of question text"
                )
                
                bg_color = st.color_picker(
                    "Background Color:",
                    "#1a1a1a",
                    help="Video background color"
                )
                
                text_color = st.color_picker(
                    "Text Color:",
                    "#ffffff",
                    help="Question and option text color"
                )
            
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🔊 Audio & Features")
                background_music = st.checkbox(
                    "Background Music",
                    value=True,
                    help="Enable background music during video"
                )
            
            with col2:
                subtitles = st.checkbox(
                    "Subtitles",
                    value=True,
                    help="Add subtitles to video"
                )
            
            with col3:
                tts = st.checkbox(
                    "Text-to-Speech",
                    value=True,
                    help="Convert questions to speech"
                )
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Settings", use_container_width=True):
                    st.session_state.video_settings = {
                        'resolution': resolution,
                        'fps': fps,
                        'duration_per_question': duration,
                        'background_music': background_music,
                        'subtitles': subtitles,
                        'transitions': transitions,
                        'text_font': text_font,
                        'font_size': font_size,
                        'background_color': bg_color,
                        'text_color': text_color
                    }
                    st.success("✓ Settings saved successfully!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.form_submit_button("🔄 Reset to Default", use_container_width=True):
                    st.session_state.video_settings = {
                        'resolution': '1080p',
                        'fps': 30,
                        'duration_per_question': 10,
                        'background_music': True,
                        'subtitles': True,
                        'transitions': 'fade',
                        'text_font': 'Arial',
                        'font_size': 24,
                        'background_color': '#1a1a1a',
                        'text_color': '#ffffff'
                    }
                    st.success("✓ Settings reset to default!")
                    time.sleep(1)
                    st.rerun()
        
        st.divider()
        st.subheader("📋 Current Settings Preview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Video Configuration:**")
            for key, value in st.session_state.video_settings.items():
                st.write(f"• {key.replace('_', ' ').title()}: `{value}`")
        
        with col2:
            st.markdown("**Video Configuration (JSON):**")
            config = generate_video_config(st.session_state.video_settings)
            st.json(config)
    
    # ==================== GENERATE VIDEO PAGE ====================
    elif page == "🎥 Generate Video":
        st.title("🎥 Generate Quiz Video")
        
        if not st.session_state.questions:
            st.warning("⚠️ No questions imported yet. Please import questions first.")
            if st.button("Go to Import Questions"):
                st.rerun()
        else:
            st.info(f"ℹ️ You have {len(st.session_state.questions)} questions ready for video generation")
            
            with st.form("video_generation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    quiz_name = st.text_input(
                        "Quiz Name:",
                        value="Quiz_Video",
                        help="Name for the generated video file"
                    )
                
                with col2:
                    output_format = st.selectbox(
                        "Output Format:",
                        ["MP4", "WebM", "MKV"],
                        help="Video file format"
                    )
                
                st.divider()
                st.markdown("### 🎬 Generation Settings")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Resolution:** {st.session_state.video_settings['resolution']}")
                    st.markdown(f"**FPS:** {st.session_state.video_settings['fps']}")
                
                with col2:
                    st.markdown(f"**Duration/Q:** {st.session_state.video_settings['duration_per_question']}s")
                    total_duration = (len(st.session_state.questions) * 
                                    st.session_state.video_settings['duration_per_question'])
                    st.markdown(f"**Est. Duration:** ~{total_duration}s ({total_duration//60}m)")
                
                with col3:
                    st.markdown(f"**Transitions:** {st.session_state.video_settings['transitions'].title()}")
                    st.markdown(f"**Subtitles:** {'Yes' if st.session_state.video_settings['subtitles'] else 'No'}")
                
                st.divider()
                
                advanced = st.checkbox("⚙️ Advanced Options")
                
                if advanced:
                    col1, col2 = st.columns(2)
                    with col1:
                        include_explanations = st.checkbox(
                            "Include Explanations",
                            value=True,
                            help="Show explanation after each answer"
                        )
                    with col2:
                        add_countdown = st.checkbox(
                            "Add Answer Countdown",
                            value=True,
                            help="Show countdown timer before answer reveal"
                        )
                
                st.divider()
                
                if st.form_submit_button("🚀 Generate Video", use_container_width=True, type="primary"):
                    st.subheader("📹 Video Generation in Progress...")
                    success, message = generate_video(
                        st.session_state.questions,
                        st.session_state.video_settings,
                        quiz_name
                    )
                    
                    if success:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success(message)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                "⬇️ Download Video",
                                data=b"video_data",
                                file_name=f"{quiz_name}.{output_format.lower()}",
                                mime=f"video/{output_format.lower()}"
                            )
                        with col2:
                            if st.button("📋 View Details"):
                                st.json(st.session_state.generation_history[-1])
                        with col3:
                            if st.button("🎥 Generate Another"):
                                st.rerun()
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error(message)
                        st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== QUESTION MANAGER PAGE ====================
    elif page == "📚 Question Manager":
        st.title("📚 Question Manager")
        
        if not st.session_state.questions:
            st.info("No questions imported yet")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Questions", len(st.session_state.questions))
            with col2:
                easy_count = sum(1 for q in st.session_state.questions if q.get('difficulty') == 'easy')
                st.metric("Easy", easy_count)
            with col3:
                hard_count = sum(1 for q in st.session_state.questions if q.get('difficulty') == 'hard')
                st.metric("Hard", hard_count)
            
            st.divider()
            
            tab1, tab2, tab3 = st.tabs(["📖 View Questions", "✏️ Edit Questions", "⬇️ Export"])
            
            with tab1:
                st.subheader("All Questions")
                
                filter_difficulty = st.selectbox(
                    "Filter by difficulty:",
                    ["All", "easy", "medium", "hard"]
                )
                
                filtered = st.session_state.questions
                if filter_difficulty != "All":
                    filtered = [q for q in filtered if q.get('difficulty') == filter_difficulty]
                
                for idx, question in enumerate(filtered, 1):
                    display_question_card(question, idx)
            
            with tab2:
                st.subheader("Edit Questions")
                
                question_idx = st.number_input(
                    "Select question to edit:",
                    1, len(st.session_state.questions), 1
                ) - 1
                
                question = st.session_state.questions[question_idx]
                
                with st.form("edit_question_form"):
                    new_question = st.text_area(
                        "Question:",
                        value=question.get('question', '')
                    )
                    
                    new_options = []
                    for i, option in enumerate(question.get('options', [])):
                        new_opt = st.text_input(f"Option {i + 1}:", value=option)
                        new_options.append(new_opt)
                    
                    new_correct = st.selectbox(
                        "Correct answer:",
                        new_options,
                        index=new_options.index(question.get('correct_answer', ''))
                    )
                    
                    new_explanation = st.text_area(
                        "Explanation:",
                        value=question.get('explanation', '')
                    )
                    
                    new_difficulty = st.selectbox(
                        "Difficulty:",
                        ["easy", "medium", "hard"],
                        index=["easy", "medium", "hard"].index(question.get('difficulty', 'medium'))
                    )
                    
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        st.session_state.questions[question_idx] = {
                            'question': new_question,
                            'options': new_options,
                            'correct_answer': new_correct,
                            'explanation': new_explanation,
                            'difficulty': new_difficulty
                        }
                        st.success("✓ Question updated!")
                        time.sleep(1)
                        st.rerun()
            
            with tab3:
                st.subheader("Export Questions")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Export as CSV", use_container_width=True):
                        csv_data = export_questions(st.session_state.questions, 'csv')
                        st.download_button(
                            "⬇️ Download CSV",
                            csv_data,
                            "questions.csv",
                            "text/csv"
                        )
                
                with col2:
                    if st.button("📥 Export as JSON", use_container_width=True):
                        json_data = export_questions(st.session_state.questions, 'json')
                        st.download_button(
                            "⬇️ Download JSON",
                            json_data,
                            "questions.json",
                            "application/json"
                        )
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Clear All Questions", use_container_width=True):
                        st.session_state.questions = []
                        st.warning("⚠️ All questions have been cleared!")
                        time.sleep(1)
                        st.rerun()
    
    # ==================== HISTORY PAGE ====================
    elif page == "📋 History":
        st.title("📋 Generation History")
        
        if not st.session_state.generation_history:
            st.info("No videos generated yet")
        else:
            st.subheader(f"Total Videos Generated: {len(st.session_state.generation_history)}")
            
            for idx, job in enumerate(st.session_state.generation_history, 1):
                with st.expander(
                    f"📹 {job['quiz_name']} - {job['timestamp'].split('T')[0]}",
                    expanded=False
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Questions", job['question_count'])
                    with col2:
                        st.metric("Status", job['status'].title())
                    with col3:
                        st.metric("Output", job['output_file'].split('/')[-1][:20] + "...")
                    
                    st.divider()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Video Settings:**")
                        for key, value in job['settings'].items():
                            st.write(f"• {key.replace('_', ' ').title()}: `{value}`")
                    
                    with col2:
                        st.markdown("**Details:**")
                        st.write(f"**Timestamp:** {job['timestamp']}")
                        st.write(f"**Output File:** {job['output_file']}")
                    
                    if st.button(f"🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.generation_history.pop(idx - 1)
                        st.success("Deleted!")
                        time.sleep(0.5)
                        st.rerun()


if __name__ == "__main__":
    main()
