import streamlit as st
import sqlite3


# Connect to the SQLite database
conn = sqlite3.connect("forum_database.db")
cursor = conn.cursor()

# Create users and topics tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS topics
                (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT)''')
                
from pathlib import Path

filename = "flag.txt"  # Replace with the name of the file you want to check
file_path = Path(filename)
st.image("STUDENTS.jpg")
if file_path.is_file():
    pass
else:
    with open("flag.txt", "w") as file:
        file.write("False")
# User registration function
def register_user():
    st.subheader("User Registration")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password == confirm_password:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            st.success("Registration successful. You can now log in.")
        else:
            st.error("Passwords do not match. Please try again.")

# User login function
def login_user():
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        #print (user)
        if user:
            st.success(f"Welcome, {username}!")
            st.subheader("Valid user Logged into forum ")
            st.empty()
            return "T"
        else:
            st.error("Invalid username or password. Please try again.")

    return "F"

# Create a new discussion topic
def create_topic():
    st.subheader("Create a New Discussion Topic")
    author=st.text_input("Author Name")
    title = st.text_input("Topic Title")
    content = st.text_area("Topic Content")

    if st.button("Create Topic"):
        cursor.execute("INSERT INTO topics (title, content, author) VALUES (?, ?, ?)", (title, content,author))
        conn.commit()
        st.success("Topic created successfully.")

# List and view discussion topics
def view_topics():
    st.subheader("Discussion Topics")
    cursor.execute("SELECT * FROM topics")
    topics = cursor.fetchall()

    if not topics:
        st.error("No topics have been discussed yet.")
    else:
        st.write("")
        for topic in topics:
            st.write(f"**{topic[1]}**")
            st.write(f"Author: {topic[3]}")
            st.write(topic[2])
            st.write("---")

# Main application
def option(selected_option):
    if selected_option == "Status":
        st.header("Valid user Logged into the system!!")
    elif selected_option == "Create_Topic":
        create_topic()
    elif selected_option == "View_Topics":
        view_topics()
    elif selected_option == "Logout":
        with open("flag.txt", "w") as file:
            file.write("False")
        pass
        #user = None

def main():
    st.title("Online Student Discussion Forum")
    st.sidebar.title("MENU")
    menu = st.sidebar.radio("Choose from the window below", ["Home", "Register", "Login"])
    
    if menu == "Home":
        st.header("Welcome to the Forum")
        st.write("Please login or register to participate.")
        with open("flag.txt", "w") as file:
            file.write("False")


    elif menu == "Register":
        register_user()

    elif menu == "Login":
        flag=login_user()
        #print(flag)
        if flag=="T":
            #print (login_user())
            with open("flag.txt", "w") as file:
                file.write("True")
        
        with open("flag.txt", "r") as file:
            value = file.read().strip()
        if value=="True":
            st.sidebar.title("User Options")
            selected_option = st.sidebar.radio("Select an option", ["Status", "Create_Topic", "View_Topics", "Logout"])
            option(selected_option)
                        
if __name__ == "__main__":
    main()

