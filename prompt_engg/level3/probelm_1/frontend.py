import streamlit as st
from backend import add_task, get_all_tasks

st.title("Student Club Task Recorder")

# Function to add a new task
def add_new_task():
    st.subheader("Add New Task")
    task_name = st.text_input("Task Name")
    task_description = st.text_area("Task Description")
    if st.button("Add Task"):
        if task_name.strip() != "":
            add_task({"name": task_name, "description": task_description})
            st.success("Task added successfully!")
        else:
            st.error("Task name cannot be empty.")

# Function to display all tasks
def display_tasks():
    st.subheader("All Tasks")
    tasks = get_all_tasks()
    if tasks:
        for task in tasks:
            st.write(f"**{task['name']}**: {task['description']}")
    else:
        st.write("No tasks found.")

add_new_task()
display_tasks()
