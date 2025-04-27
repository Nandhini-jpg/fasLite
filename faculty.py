import streamlit as st
import pandas as pd
from auth import get_current_user
from data_manager import (
    get_faculty_publications, add_publication, update_publication, delete_publication,
    get_faculty_experiences, add_experience, update_experience, delete_experience,
    get_feedback_summary
)

def faculty_dashboard():
    user = get_current_user()
    
    # Tab navigation
    tabs = st.tabs(["Publications", "Experiences", "Feedback"])
    
    # Publications Tab
    with tabs[0]:
        st.header("My Publications")
        
        # Get existing publications
        publications = get_faculty_publications(user['username'])
        
        # Add new publication form
        with st.expander("Add New Publication", expanded=False):
            with st.form("publication_form"):
                pub_title = st.text_input("Title")
                pub_journal = st.text_input("Journal Name")
                pub_year = st.number_input("Year", min_value=1900, max_value=2100, value=2023)
                pub_doi = st.text_input("DOI")
                
                submit_button = st.form_submit_button("Add Publication")
                
                if submit_button:
                    if pub_title and pub_journal and pub_year and pub_doi:
                        add_publication(user['username'], pub_title, pub_journal, pub_year, pub_doi)
                        st.success("Publication added successfully!")
                        st.rerun()
                    else:
                        st.error("All fields are required.")
        
        # Display existing publications
        if not publications:
            st.info("You haven't added any publications yet.")
        else:
            for i, pub in enumerate(publications):
                with st.expander(f"{pub['title']} ({pub['year']})", expanded=False):
                    # View mode
                    st.write(f"**Journal:** {pub['journal']}")
                    st.write(f"**DOI:** {pub['doi']}")
                    st.write(f"**Year:** {pub['year']}")
                    
                    # Edit/Delete actions
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_clicked = st.button("Edit", key=f"edit_pub_{pub['id']}")
                    with col2:
                        delete_clicked = st.button("Delete", key=f"delete_pub_{pub['id']}")
                    
                    # Handle delete
                    if delete_clicked:
                        delete_publication(pub['id'])
                        st.success("Publication deleted!")
                        st.rerun()
                    
                    # Edit form (shows up when edit is clicked)
                    if edit_clicked:
                        with st.form(f"edit_pub_form_{pub['id']}"):
                            edit_title = st.text_input("Title", value=pub['title'])
                            edit_journal = st.text_input("Journal Name", value=pub['journal'])
                            edit_year = st.number_input("Year", min_value=1900, max_value=2100, value=pub['year'])
                            edit_doi = st.text_input("DOI", value=pub['doi'])
                            
                            update_button = st.form_submit_button("Update Publication")
                            
                            if update_button:
                                if edit_title and edit_journal and edit_year and edit_doi:
                                    update_publication(pub['id'], edit_title, edit_journal, edit_year, edit_doi)
                                    st.success("Publication updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("All fields are required.")
                                    
    # Experiences Tab
    with tabs[1]:
        st.header("My Teaching & Industry Experience")
        
        # Get existing experiences
        experiences = get_faculty_experiences(user['username'])
        
        # Add new experience form
        with st.expander("Add New Experience", expanded=False):
            with st.form("experience_form"):
                exp_institution = st.text_input("Institution/Company Name")
                exp_role = st.text_input("Role/Position")
                exp_duration = st.text_input("Duration (e.g., 2018-2022)")
                exp_description = st.text_area("Description")
                
                submit_button = st.form_submit_button("Add Experience")
                
                if submit_button:
                    if exp_institution and exp_role and exp_duration:
                        add_experience(user['username'], exp_institution, exp_role, exp_duration, exp_description)
                        st.success("Experience added successfully!")
                        st.rerun()
                    else:
                        st.error("Institution, Role, and Duration are required.")
        
        # Display existing experiences
        if not experiences:
            st.info("You haven't added any experiences yet.")
        else:
            for i, exp in enumerate(experiences):
                with st.expander(f"{exp['role']} at {exp['institution']}", expanded=False):
                    # View mode
                    st.write(f"**Duration:** {exp['duration']}")
                    st.write(f"**Description:** {exp['description']}")
                    
                    # Edit/Delete actions
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_clicked = st.button("Edit", key=f"edit_exp_{exp['id']}")
                    with col2:
                        delete_clicked = st.button("Delete", key=f"delete_exp_{exp['id']}")
                    
                    # Handle delete
                    if delete_clicked:
                        delete_experience(exp['id'])
                        st.success("Experience deleted!")
                        st.rerun()
                    
                    # Edit form (shows up when edit is clicked)
                    if edit_clicked:
                        with st.form(f"edit_exp_form_{exp['id']}"):
                            edit_institution = st.text_input("Institution/Company Name", value=exp['institution'])
                            edit_role = st.text_input("Role/Position", value=exp['role'])
                            edit_duration = st.text_input("Duration", value=exp['duration'])
                            edit_description = st.text_area("Description", value=exp['description'])
                            
                            update_button = st.form_submit_button("Update Experience")
                            
                            if update_button:
                                if edit_institution and edit_role and edit_duration:
                                    update_experience(exp['id'], edit_institution, edit_role, edit_duration, edit_description)
                                    st.success("Experience updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("Institution, Role, and Duration are required.")
    
    # Feedback Tab
    with tabs[2]:
        st.header("Feedback Received")
        
        # Get feedback summary
        feedback_summary = get_feedback_summary(user['username'])
        
        # Display feedback summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", f"{feedback_summary['avg_rating']} / 5.0")
        with col2:
            st.metric("From Students", feedback_summary['student_count'])
        with col3:
            st.metric("From Dean", feedback_summary['dean_count'])
        
        # Display individual feedback
        if not feedback_summary['feedback']:
            st.info("You haven't received any feedback yet.")
        else:
            st.write("### Individual Feedback")
            for feedback in feedback_summary['feedback']:
                source = "Dean" if feedback['dean_username'] else "Student"
                with st.container():
                    st.markdown(f"**From:** {source} | **Rating:** {feedback['rating']}/5 | **Date:** {feedback['timestamp']}")
                    st.markdown(f"**Semester:** {feedback['semester']}")
                    if feedback['comment']:
                        st.markdown(f"**Comment:** {feedback['comment']}")
                    st.divider()
