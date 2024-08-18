import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

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

# Function to delete a group
def delete_group(groups):
    group_num = st.number_input("Enter the group number you want to delete:", min_value=1, max_value=len(groups), step=1)
    if st.button("Delete Group"):
        del groups[group_num - 1]
        st.success(f"Group {group_num} has been deleted.")

# Function to compute common skills among group members
def compute_common_skills(group, students):
    all_skills = [skill for member in group for skill in students[member]]
    common_skills = pd.Series(all_skills).value_counts().head(5)
    return common_skills

# Function to visualize the most common skills among students
def visualize_common_skills(students):
    all_skills = [skill for skills_list in students.values() for skill in skills_list]
    common_skills = pd.Series(all_skills).value_counts().head(5)
    
    # Plotting
    st.write("Most Common Skills Among Students:")
    st.bar_chart(common_skills)

# Function to plot a pie chart of skills distribution
def plot_skills_pie_chart(students):
    all_skills = [skill for skills_list in students.values() for skill in skills_list]
    skill_counts = pd.Series(all_skills).value_counts()
    
    # Create a Plotly pie chart figure
    fig = px.pie(skill_counts, values=skill_counts.values, names=skill_counts.index, title='Skills Distribution Among Students')
    
    # Display the Plotly pie chart
    st.plotly_chart(fig, use_container_width=True)

# Main function
def main():
    # Read student data and generate groups
    file_path = 'students_100.csv'
    min_group_size = st.slider("Minimum Group Size:", 1, 10, 3)
    max_group_size = st.slider("Maximum Group Size:", min_group_size, 20, 5)
    students = read_student_data(file_path)
    groups = create_groups(students, min_group_size, max_group_size)

    # Display generated groups
    st.write('Generated Groups:')
    for i, group in enumerate(groups, 1):
        st.write(f'Group {i}: {", ".join(group)}')

    # Delete a group
    delete_group(groups)

    # Display remaining groups
    st.write('\nRemaining Groups:')
    for i, group in enumerate(groups, 1):
        st.write(f'Group {i}: {", ".join(group)}')

    # Visualize common skills among students
    visualize_common_skills(students)

    # Plot skills distribution among students as a pie chart
    plot_skills_pie_chart(students)

if __name__ == "__main__":
    main()
