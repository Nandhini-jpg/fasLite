import streamlit as st
import pandas as pd
from auth import get_current_user
from data_manager import (
    get_all_faculty, get_faculty_publications, get_faculty_experiences,
    get_feedback_summary, add_feedback, get_current_semester
)

def dean_dashboard():
    user = get_current_user()
    
    st.header("Faculty Management Dashboard")
    
    # Get list of all faculty
    faculty_list = get_all_faculty()
    
    if not faculty_list:
        st.warning("No faculty members are registered in the system.")
    else:
        # Create a dropdown to select faculty
        faculty_names = [f['name'] for f in faculty_list]
        faculty_usernames = [f['username'] for f in faculty_list]
        
        selected_faculty_index = st.selectbox(
            "Select Faculty Member to View/Provide Feedback",
            range(len(faculty_list)),
            format_func=lambda i: faculty_names[i]
        )
        
        selected_faculty_username = faculty_usernames[selected_faculty_index]
        selected_faculty_name = faculty_names[selected_faculty_index]
        
        st.subheader(f"Information for {selected_faculty_name}")
        
        # Tab navigation for selected faculty
        tabs = st.tabs(["Publications", "Experience", "Feedback"])
        
        # Publications Tab
        with tabs[0]:
            st.write("### Publications")
            publications = get_faculty_publications(selected_faculty_username)
            
            if not publications:
                st.info(f"{selected_faculty_name} hasn't added any publications yet.")
            else:
                pub_df = pd.DataFrame(publications)
                pub_df = pub_df[['title', 'journal', 'year', 'doi']]
                st.dataframe(pub_df, use_container_width=True)
        
        # Experiences Tab
        with tabs[1]:
            st.write("### Experience")
            experiences = get_faculty_experiences(selected_faculty_username)
            
            if not experiences:
                st.info(f"{selected_faculty_name} hasn't added any experiences yet.")
            else:
                for exp in experiences:
                    with st.expander(f"{exp['role']} at {exp['institution']}", expanded=False):
                        st.write(f"**Duration:** {exp['duration']}")
                        st.write(f"**Description:** {exp['description']}")
        
        # Feedback Tab
        with tabs[2]:
            st.write("### Feedback Summary")
            
            # Get feedback summary
            feedback_summary = get_feedback_summary(selected_faculty_username)
            
            # Display feedback stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Rating", f"{feedback_summary['avg_rating']} / 5.0")
            with col2:
                st.metric("From Students", feedback_summary['student_count'])
            with col3:
                st.metric("From Dean", feedback_summary['dean_count'])
            
            # Provide feedback form
            st.write("### Provide Feedback")
            
            feedback_already_given = False
            for feedback in feedback_summary['feedback']:
                if feedback['dean_username'] == user['username'] and feedback['semester'] == get_current_semester():
                    feedback_already_given = True
                    st.info("You have already provided feedback for this faculty this semester, but you can update it.")
                    break
            
            with st.form("dean_feedback_form"):
                st.write(f"Providing feedback for: **{selected_faculty_name}**")
                st.write(f"Current Semester: **{get_current_semester()}**")
                
                rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
                comment = st.text_area("Comments (optional)")
                
                submit_button = st.form_submit_button("Submit Feedback")
                
                if submit_button:
                    success, message = add_feedback(
                        from_username=user['username'],
                        from_role='dean',
                        faculty_username=selected_faculty_username,
                        rating=rating,
                        comment=comment,
                        semester=get_current_semester()
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
