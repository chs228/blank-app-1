import streamlit as st
import google.generativeai as genai
import joblib
import time
import os
import random
from datetime import datetime

# Configure Gemini AI
genai.configure(api_key="AIzaSyCx70_PG_V6tkCsarNnIP9qs_fl5THZIMI")
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_content(prompt, topic):
    try:
        response = model.generate_content(f"{prompt} about {topic}")
        return response.text if response.text else "Error: No response received"
    except Exception as e:
        return f"Error generating content: {str(e)}"

def save_progress(username, progress):
    joblib.dump(progress, f"{username}_progress.joblib")

def load_progress(username):
    if os.path.exists(f"{username}_progress.joblib"):
        return joblib.load(f"{username}_progress.joblib")
    return {}

def generate_quiz(topic, level):
    prompt = f"""Generate a multiple-choice quiz for level {level} students about {topic}.
    Format:
    Question: [Question text]
    A. [Option A]
    B. [Option B]
    C. [Option C]
    D. [Option D]
    Correct Answer: [A/B/C/D]
    Explanation: [Brief explanation of the correct answer]
    Generate 3 questions in this format."""
    
    quiz_content = generate_content(prompt, topic)
    if "Error" in quiz_content or not quiz_content.strip():
        return ["Error: Quiz generation failed"]
    
    print(f"Generated Quiz:\n{quiz_content}")  # Debugging
    return quiz_content.split("\n\n")

def parse_quiz_question(question):
    lines = question.split("\n")
    if len(lines) < 7:
        return {"error": "Invalid question format", "raw": question}
    
    try:
        return {
            "question": lines[0].split(": ", 1)[1] if ": " in lines[0] else "Invalid format",
            "options": {
                "A": lines[1][3:] if len(lines) > 1 else "N/A",
                "B": lines[2][3:] if len(lines) > 2 else "N/A",
                "C": lines[3][3:] if len(lines) > 3 else "N/A",
                "D": lines[4][3:] if len(lines) > 4 else "N/A",
            },
            "correct": lines[5].split(": ", 1)[1] if len(lines) > 5 and ": " in lines[5] else "Unknown",
            "explanation": lines[6].split(": ", 1)[1] if len(lines) > 6 and ": " in lines[6] else "No explanation provided"
        }
    except IndexError:
        return {"error": "Parsing error", "raw": question}

def main():
    st.title("Gemini AI: Personalized Learning Companion")
    
    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if not st.session_state.username:
        st.session_state.username = st.text_input("Enter your username:")
    
    if st.session_state.username:
        progress = load_progress(st.session_state.username)
        
        st.sidebar.header("Learning Dashboard")
        topic = st.sidebar.selectbox("Select a topic:", ["Math", "Science", "History", "Literature"])
        
        if topic:
            if topic not in progress:
                progress[topic] = {"level": 1, "score": 0, "last_study": None}
            
            level = progress[topic]["level"]
            score = progress[topic]["score"]
            last_study = progress[topic]["last_study"]
            
            st.sidebar.write(f"Current Level: {level}")
            st.sidebar.write(f"Current Score: {score}/100")
            if last_study:
                st.sidebar.write(f"Last studied: {last_study}")
            
            tab1, tab2, tab3 = st.tabs(["Lesson", "Quiz", "AI Tutor"])
            
            with tab1:
                st.header(f"Learning {topic}")
                content = generate_content(f"Generate a comprehensive lesson for level {level} students", topic)
                if "Error" in content:
                    st.error(content)
                else:
                    st.write(content)
                
                if st.button("Mark as Completed"):
                    progress[topic]["score"] += 5
                    progress[topic]["last_study"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("Lesson marked as completed! +5 points")
            
            with tab2:
                st.header("Quiz Time!")
                if 'current_quiz' not in st.session_state:
                    st.session_state.current_quiz = generate_quiz(topic, level)
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                
                if st.session_state.quiz_index < len(st.session_state.current_quiz):
                    question = parse_quiz_question(st.session_state.current_quiz[st.session_state.quiz_index])
                    
                    if "error" in question:
                        st.error(f"Quiz format error: {question['error']}")
                        st.write("Raw Data:", question["raw"])
                    else:
                        st.write(question["question"])
                        user_answer = st.radio("Select your answer:", list(question["options"].keys()), format_func=lambda x: question["options"][x])
                        
                        if st.button("Submit Answer"):
                            if user_answer == question["correct"]:
                                st.success("Correct! " + question["explanation"])
                                st.session_state.quiz_score += 1
                            else:
                                st.error(f"Incorrect. The correct answer is {question['correct']}. " + question["explanation"])
                            st.session_state.quiz_index += 1
                            
                            if st.session_state.quiz_index >= len(st.session_state.current_quiz):
                                final_score = st.session_state.quiz_score / len(st.session_state.current_quiz) * 100
                                st.write(f"Quiz completed! Your score: {final_score:.2f}%")
                                progress[topic]["score"] += int(final_score / 2)
                                if progress[topic]["score"] >= 100:
                                    progress[topic]["level"] += 1
                                    progress[topic]["score"] = 0
                                    st.balloons()
                                    st.success(f"Congratulations! You've advanced to level {progress[topic]['level']}!")
                                del st.session_state.current_quiz
                else:
                    if st.button("Take Another Quiz"):
                        del st.session_state.current_quiz
                        st.experimental_rerun()
            
            with tab3:
                st.header("Chat with AI Tutor")
                user_question = st.text_input("Ask your question:")
                if user_question:
                    response = generate_content(f"Answer this question: {user_question}", topic)
                    st.write("AI Tutor:")
                    st.write(response)
            
            save_progress(st.session_state.username, progress)
        
        if st.sidebar.button("Log Out"):
            st.session_state.username = ''
            st.experimental_rerun()

if __name__ == "__main__":
    main()
