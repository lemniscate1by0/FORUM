import streamlit as st
import sqlite3
from pathlib import Path

# Connect to the SQLite database
conn = sqlite3.connect("forum_database.db")
cursor = conn.cursor()

# Create users and topics tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS topics
                (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT)''')
   
cursor.execute('''CREATE TABLE IF NOT EXISTS replies
                (id INTEGER PRIMARY KEY, topic_id INTEGER, reply TEXT,author TEXT)''')             


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



# ... (previous code)

def reply_to_topic(topic_id):
    st.subheader("Reply to Topic")
    author_key = f"AuthorName_{topic_id}"
    reply_key = f"ReplyContent_{topic_id}"
    
    author = st.text_input("Author Name", key=author_key)
    reply_content = st.text_area("Your Reply", key=reply_key)

    if st.button(f"Submit Reply_{topic_id}"):
        cursor.execute("INSERT INTO replies (topic_id, reply, author) VALUES (?, ?, ?)", (topic_id, reply_content, author))
        conn.commit()
        st.success("Reply posted successfully.")

def view_replies(topic_id):
    st.subheader("Replies to the Topic")
    cursor.execute("SELECT * FROM replies WHERE topic_id = ?", (topic_id,))
    replies = cursor.fetchall()

    if not replies:
        st.error("No replies for this topic yet.")
    else:
        for reply in replies:
            st.write(f"Author: {reply[3]}")
            st.write(reply[2])
            st.write("---")

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

            # Add a "Reply" button for each topic
            reply_button_key = f"Reply_{topic[0]}"
            reply_form_key = f"ReplyForm_{topic[0]}"
            
            # Button to toggle visibility of reply form
            if st.button(f"Reply to Topic #{topic[0]}", key=reply_button_key):
                st.session_state[reply_form_key] = not st.session_state.get(reply_form_key, False)

            # Display reply form if the button is clicked
            if st.session_state.get(reply_form_key, False):
                reply_to_topic(topic[0])

            # Display replies
            view_replies(topic[0])

            st.write("---")

# ... (remaining code)




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

