import streamlit as st
import pandas as pd
from auth import get_current_user
from data_manager import (
    get_all_faculty, add_feedback, has_given_feedback, 
    get_current_semester
)

def student_dashboard():
    user = get_current_user()
    
    st.header("Faculty Feedback Dashboard")
    
    # Get list of all faculty
    faculty_list = get_all_faculty()
    
    if not faculty_list:
        st.warning("No faculty members are registered in the system.")
    else:
        st.subheader("Provide Feedback for Faculty")
        st.write(f"Current Semester: **{get_current_semester()}**")
        
        # Create a dropdown to select faculty
        faculty_names = [f['name'] for f in faculty_list]
        faculty_usernames = [f['username'] for f in faculty_list]
        
        selected_faculty_index = st.selectbox(
            "Select Faculty Member",
            range(len(faculty_list)),
            format_func=lambda i: faculty_names[i]
        )
        
        selected_faculty_username = faculty_usernames[selected_faculty_index]
        selected_faculty_name = faculty_names[selected_faculty_index]
        
        # Check if student has already given feedback for this faculty this semester
        current_semester = get_current_semester()
        already_submitted = has_given_feedback(user['username'], selected_faculty_username, current_semester)
        
        if already_submitted:
            st.warning(f"You have already submitted feedback for {selected_faculty_name} this semester ({current_semester}).")
        else:
            st.write(f"Providing feedback for: **{selected_faculty_name}**")
            
            with st.form("student_feedback_form"):
                rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
                comment = st.text_area("Comments (optional)")
                
                submit_button = st.form_submit_button("Submit Feedback")
                
                if submit_button:
                    success, message = add_feedback(
                        from_username=user['username'],
                        from_role='student',
                        faculty_username=selected_faculty_username,
                        rating=rating,
                        comment=comment,
                        semester=current_semester
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                        
        # Show a list of faculty for whom the student has already provided feedback
        st.subheader("Faculty Feedback Status")
        
        feedback_status = []
        for i, faculty in enumerate(faculty_list):
            status = "Submitted" if has_given_feedback(user['username'], faculty['username'], current_semester) else "Not Submitted"
            feedback_status.append({
                "Faculty Name": faculty['name'],
                "Feedback Status": status,
                "Semester": current_semester
            })
        
        status_df = pd.DataFrame(feedback_status)
        st.dataframe(status_df, use_container_width=True)
