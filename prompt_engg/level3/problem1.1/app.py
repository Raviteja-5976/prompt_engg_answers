
import streamlit as st
import sqlite3
from datetime import datetime

# Create or connect to the SQLite database
conn = sqlite3.connect('team_reports.db')
c = conn.cursor()

# Create the "members" table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY,
        name TEXT,
        roll_number TEXT,
        phone_number TEXT,
        email TEXT,
        year TEXT,
        course_name TEXT,
        designation TEXT
    )
''')

# Create the "tasks" table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        member_id INTEGER,
        task_name TEXT,
        assigned_on DATE,
        status TEXT,
        completed_on DATE,
        comment TEXT,
        FOREIGN KEY (member_id) REFERENCES members(id)
    )
''')

def main():
    st.title("GDSE MANAGEMENT TEAM")

    # Create tabs
    tabs = ["Details Entry", "Task Entry", "List of Tasks"]
    choice = st.sidebar.selectbox("Select Tab", tabs)

    if choice == "Details Entry":
        details_entry_tab()
    elif choice == "Task Entry":
        task_entry_tab()
    elif choice == "List of Tasks":
        list_of_tasks_tab()
    # elif choice == "Delete a Member":
    #     delete()



def details_entry_tab():
    st.header("Details Entry")
    name = st.text_input("Name")
    roll_number = st.text_input("Roll Number")
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email")
    year = st.text_input("Year")
    course_name = st.text_input("Course Name")
    designation = st.text_input("Designation")

    if st.button("Add Member"):
        c.execute('''
            INSERT INTO members (name, roll_number, phone_number, email, year, course_name, designation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, roll_number, phone_number, email, year, course_name, designation))
        conn.commit()
        st.success("Member added successfully!")

def task_entry_tab():
    st.header("Task Entry")
    member_id = st.selectbox("Select Member", c.execute("SELECT id, name FROM members").fetchall())
    task_name = st.text_input("Task Name")
    assigned_on = st.date_input("Assigned On", datetime.today())
    status = st.selectbox("Status", ["To Do", "In Progress", "Completed"])
    completed_on = st.date_input("Completed On", datetime.today() if status == "Completed" else None)
    comment = st.text_area("comment")

    if st.button("Add Task"):
        c.execute('''
            INSERT INTO tasks (member_id, task_name, assigned_on, status, completed_on, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (member_id[0], task_name, assigned_on, status, completed_on, comment))
        conn.commit()
        st.success("Task added successfully!")

#
def list_of_tasks_tab():
    st.header("List of Tasks")
    member_id = st.selectbox("Select Member", c.execute("SELECT id, name FROM members").fetchall())

    # Display member details
    member_details = c.execute('''
        SELECT name, roll_number, phone_number, email, year, course_name, designation
        FROM members
        WHERE id = ?
    ''', (member_id[0],)).fetchone()
    
    


    st.subheader("Member Details")
    st.write("Name: {}".format(member_details[0]))
    st.write("Roll Number: {}".format(member_details[1]))
    st.write("Phone Number: {}".format(member_details[2]))
    st.write("Email: {}".format(member_details[3]))
    st.write("Year: {}".format(member_details[4]))
    st.write("Course Name: {}".format(member_details[5]))
    st.write("Designation: {}".format(member_details[6]))


    edit_member = st.checkbox('Edit Member Details')
    if edit_member:
        edit_name = st.text_input("Name:", member_details[0])
        edit_roll_number = st.text_input("Roll Number:", member_details[1])
        edit_phone_number = st.text_input("Phone Number:", member_details[2])
        edit_email = st.text_input("Email:", member_details[3])
        edit_Year = st.text_input("Year:", member_details[4])
        edit_course_name = st.text_input("Course Name:", member_details[5])
        edit_designation = st.text_input("Designation", member_details[6])
        if st.button("Update"):
            c.execute('''
                    UPDATE members
                    SET name = ?, roll_number = ?, phone_number = ?, email = ?, year = ?, course_name = ?, designation = ?
                    WHERE id = ?
            ''', (edit_name , edit_roll_number, edit_phone_number, edit_email, edit_Year, edit_course_name, edit_designation, member_id[0]))
            conn.commit()
            st.success("Updated Sucessfully!")


                


    # Filter tasks by assigned on date range
    from_date = st.date_input("From Date", key=None)
    to_date = st.date_input("To Date", key=None)

    # Display tasks for the selected member based on the date range filter
    if from_date is None and to_date is None:
        tasks = c.execute('''
            SELECT id, task_name, assigned_on, status, completed_on, comment
            FROM tasks
            WHERE member_id = ?
        ''', (member_id[0],)).fetchall()
    else:
        tasks = c.execute('''
            SELECT id, task_name, assigned_on, status, completed_on, comment
            FROM tasks
            WHERE member_id = ? AND (? IS NULL OR assigned_on >= ?) AND (? IS NULL OR assigned_on <= ?)
        ''', (member_id[0], from_date, from_date, to_date, to_date)).fetchall()

    tss = st.subheader("Tasks for {}".format(member_details[0]))
    for task in tasks:
        st.write("Task: {}".format(task[1]))
        st.write("Assigned On: {}".format(task[2]))
        st.write("Status: {}".format(task[3]))
        st.write("Completed On: {}".format(task[4]))
        st.write("Comment: {}".format(task [5]))
        
        delete_task = st.checkbox("Delete Task", key="delete_{}".format(task[0]))
        edit_task = st.checkbox("Edit Task", key="edit_{}".format(task[0]))
        if edit_task:
            edit_status = st.selectbox("Edit Status", ["To Do", "In Progress", "Completed"], index=["To Do", "In Progress", "Completed"].index(task[3]))
            edit_completed_on = st.date_input("Edit Completed On", task[4] if task[3] == "Completed" else None)
            edit_comment = st.text_area("Comment", task[5])

            if st.button("Update Task"):
                c.execute('''
                    UPDATE tasks
                    SET status = ?, completed_on = ?, comment = ?
                    WHERE id = ?
                ''', (edit_status, edit_completed_on, edit_comment, task[0]))
                conn.commit()
                st.success("Task updated successfully!")
        elif delete_task:
            if st.button("Confirm Delete Task"):
                c.execute('''
                    DELETE FROM tasks
                    WHERE id = ?
                ''', (task[0],))
                conn.commit()
                st.success("Task deleted successfully!")                

        st.write("-" * 50)

# def delete():
#     member_id = st.selectbox("Select Member", c.execute("SELECT id, name FROM members").fetchall())    
#     delete_member = st.button("Delete Member")
#     if delete_member:
#         if st.button("Confirm Delete Member"):
#             c.execute('''
#                 DELETE FROM members
#                 WHERE id = ?
#             ''', (member_id[0],))
#             conn.commit()
#             st.success("Member deleted successfully!")

st.caption("Website Created by Raviteja")


if __name__ == "__main__":
    main()

