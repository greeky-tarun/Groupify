import streamlit as st
import pandas as pd
import numpy as np

# Function to read student data from CSV file
def read_student_data(file_path):
    data = pd.read_csv(file_path)
    students = {}
    for index, row in data.iterrows():
        students[row['Student']] = row['Skills'].split(', ')
    return students

# Function to create groups of students
def create_groups(students, min_group_size, max_group_size):
    student_list = list(students.keys())
    np.random.shuffle(student_list)
    groups = []
    for i in range(0, len(student_list), max_group_size):
        group = student_list[i:i+max_group_size]
        if len(group) >= min_group_size:
            groups.append(group)
    return groups

# Main function
def main():
    # Read student data and generate groups
    file_path = 'students_100.csv'
    min_group_size = st.sidebar.slider("Minimum Group Size", 1, 10, 3)
    max_group_size = st.sidebar.slider("Maximum Group Size", min_group_size, 20, 5)
    students = read_student_data(file_path)
    groups = create_groups(students, min_group_size, max_group_size)

    # Display generated groups
    st.title('Generated Groups')
    for i, group in enumerate(groups, 1):
        st.subheader(f'Group {i}')
        members = ", ".join(group)
        st.write(f"Members: {members}")

if __name__ == "__main__":
    main()
