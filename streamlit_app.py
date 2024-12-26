import streamlit as st
import pandas as pd
from datetime import datetime

# In-memory user data for authentication
USERS = {
    "teacher": {"password": "teacher123", "role": "teacher"},
    "student123":{"password": "student", "role": "student"}
}

# Allow students to create accounts dynamically
if "student_accounts" not in st.session_state:
    st.session_state["student_accounts"] = {}

# Authentication function
def authenticate(username, password):
    user = USERS.get(username) or st.session_state["student_accounts"].get(username)
    if user and user["password"] == password:
        return user["role"]
    return None

# Function to display the login page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    login_button = st.button("Login")
    create_account_button = st.button("Create Student Account")

    if login_button:
        role = authenticate(username, password)
        if role:
            st.session_state["authenticated"] = True
            st.session_state["role"] = role
            st.session_state["username"] = username
            st.success(f"Logged in as {role.capitalize()}!")
        else:
            st.error("Invalid username or password.")

    if create_account_button:
        new_username = st.text_input("New Username:", key="new_username")
        new_password = st.text_input("New Password:", type="password", key="new_password")
        if st.button("Create Account", key="create_account"):
            if new_username in USERS or new_username in st.session_state["student_accounts"]:
                st.error("Username already exists. Please choose a different username.")
            else:
                st.session_state["student_accounts"][new_username] = {
                    "password": new_password,
                    "role": "student",
                }
                st.success("Student account created successfully! You can now log in.")

# Function to display the home page
def home_page():
    st.title("Quiz Management System")
    st.markdown(
        "Welcome to the Quiz Management System! Use the sidebar to navigate to different features of the application."
    )

# Function to create a quiz (accessible only to teachers)
def create_quiz():
    if st.session_state.get("role") != "teacher":
        st.error("Access Denied: Only teachers can create quizzes.")
        return

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

# Function to display and manage scheduled quizzes (accessible only to teachers)
def view_quizzes():
    if st.session_state.get("role") != "teacher":
        st.error("Access Denied: Only teachers can view and manage quizzes.")
        return

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

# Function to display quizzes for students
def student_quizzes():
    if st.session_state.get("role") != "student":
        st.error("Access Denied: Only students can view and attempt quizzes.")
        return

    st.title("Take a Quiz")

    # Dummy quiz data for students
    quizzes = ["Math Test", "Science Quiz"]
    selected_quiz = st.selectbox("Select a Quiz to Take:", quizzes)

    st.markdown(f"### Quiz: {selected_quiz}")
    st.markdown("(Quiz functionality can be implemented here.)")

# Function to display results (accessible to all users)
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
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["username"] = None

if not st.session_state["authenticated"]:
    login_page()
else:
    st.sidebar.title("Navigation")
    option = st.sidebar.radio(
        "Go to:", ["Home", "Create Quiz", "View Quizzes", "Take Quiz", "View Results", "Logout"]
    )

    if option == "Home":
        home_page()
    elif option == "Create Quiz":
        create_quiz()
    elif option == "View Quizzes":
        view_quizzes()
    elif option == "Take Quiz":
        student_quizzes()
    elif option == "View Results":
        view_results()
    elif option == "Logout":
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["username"] = None
        st.success("Logged out successfully!")
