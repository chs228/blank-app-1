import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to display the home page
def home_page():
    st.title("Quiz Management System")
    st.markdown(
        "Welcome to the Quiz Management System! Use the sidebar to navigate to different features of the application."
    )

# Function to create a quiz
def create_quiz():
    st.title("Create a Quiz")

    quiz_name = st.text_input("Enter the Quiz Name:")
    scheduled_date = st.date_input("Schedule Date:", min_value=datetime.today().date())
    scheduled_time = st.time_input("Schedule Time:", value=datetime.now().time())

    st.subheader("Add Questions")
    num_questions = st.number_input("Number of Questions:", min_value=1, max_value=50, step=1)

    questions = []
    for i in range(1, num_questions + 1):
        st.markdown(f"**Question {i}:**")
        question = st.text_area(f"Enter Question {i}:")
        option_a = st.text_input(f"Option A for Question {i}:")
        option_b = st.text_input(f"Option B for Question {i}:")
        option_c = st.text_input(f"Option C for Question {i}:")
        option_d = st.text_input(f"Option D for Question {i}:")
        correct_answer = st.selectbox(
            f"Select Correct Answer for Question {i}:", ["A", "B", "C", "D"], key=f"answer_{i}"
        )

        questions.append(
            {
                "question": question,
                "options": {"A": option_a, "B": option_b, "C": option_c, "D": option_d},
                "correct_answer": correct_answer,
            }
        )

    if st.button("Save Quiz"):
        quiz_data = {
            "quiz_name": quiz_name,
            "scheduled_date": scheduled_date,
            "scheduled_time": scheduled_time,
            "questions": questions,
        }
        st.success("Quiz saved successfully!")
        st.json(quiz_data)  # Display saved quiz data for debugging

# Function to display and manage scheduled quizzes
def view_quizzes():
    st.title("View Scheduled Quizzes")

    # Dummy data for illustration
    quizzes = pd.DataFrame(
        {
            "Quiz Name": ["Math Test", "Science Quiz"],
            "Scheduled Date": ["2024-12-27", "2024-12-28"],
            "Scheduled Time": ["10:00 AM", "02:00 PM"],
        }
    )

    st.dataframe(quizzes)

    st.markdown("### Actions")
    selected_quiz = st.selectbox("Select a Quiz to Manage:", quizzes["Quiz Name"].tolist())
    if st.button("Delete Selected Quiz"):
        st.warning(f"Deleted quiz: {selected_quiz}")

# Function to display results
def view_results():
    st.title("View Results")

    # Dummy results data
    results = pd.DataFrame(
        {
            "Student Name": ["Alice", "Bob"],
            "Quiz Name": ["Math Test", "Science Quiz"],
            "Score": ["80%", "90%"],
        }
    )

    st.dataframe(results)

# Streamlit sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Go to:", ["Home", "Create Quiz", "View Quizzes", "View Results"]
)

if option == "Home":
    home_page()
elif option == "Create Quiz":
    create_quiz()
elif option == "View Quizzes":
    view_quizzes()
elif option == "View Results":
    view_results()
