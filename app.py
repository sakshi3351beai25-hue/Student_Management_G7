
import streamlit as st
import pandas as pd

st.title("Student Record Management System")

# Initialize student records
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course", "Marks"]
    )

st.sidebar.title("Menu")
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add Student Record")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Add Student"):
        if name.strip() and course.strip():
            if roll not in st.session_state.students["Roll No"].values:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                st.session_state.students = pd.concat(
                    [st.session_state.students, new_student],
                    ignore_index=True
                )
                st.success("Student added successfully!")
            else:
                st.error("Roll Number already exists!")
        else:
            st.warning("Please enter Name and Course.")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    if not st.session_state.students.empty:
        st.dataframe(st.session_state.students)
    else:
        st.info("No student records found.")

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Record")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())

        student = df[df["Roll No"] == roll].iloc[0]

        name = st.text_input("Name", value=student["Name"])
        age = st.number_input("Age", min_value=1, max_value=100,
                              value=int(student["Age"]))
        course = st.text_input("Course", value=student["Course"])
        marks = st.number_input("Marks", min_value=0, max_value=100,
                                value=int(student["Marks"]))

        if st.button("Update Student"):
            idx = df[df["Roll No"] == roll].index[0]

            st.session_state.students.loc[idx, "Name"] = name
            st.session_state.students.loc[idx, "Age"] = age
            st.session_state.students.loc[idx, "Course"] = course
            st.session_state.students.loc[idx, "Marks"] = marks

            st.success("Student record updated successfully!")
    else:
        st.info("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number to Delete",
                            df["Roll No"].tolist())

        if st.button("Delete Student"):
            st.session_state.students = df[
                df["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")
    else:
        st.info("No records available to delete.")