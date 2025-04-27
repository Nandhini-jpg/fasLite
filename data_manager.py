import streamlit as st
import pandas as pd
from datetime import datetime
from db_setup import get_db_session, User, Publication, Experience, Feedback

def initialize_data():
    """Initialize sample data structures if they don't exist"""
    # Current semester is still stored in session state for convenience
    if 'current_semester' not in st.session_state:
        # Format: Year-Semester (1 for Spring, 2 for Fall)
        current_year = datetime.now().year
        current_month = datetime.now().month
        semester = 1 if current_month < 7 else 2
        st.session_state.current_semester = f"{current_year}-{semester}"

def get_user_by_username(username):
    """Get a user by username"""
    session = get_db_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user

def get_user_by_id(user_id):
    """Get a user by ID"""
    session = get_db_session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user

def get_all_faculty():
    """Get list of all faculty members"""
    session = get_db_session()
    faculty_users = session.query(User).filter(User.role == 'faculty').all()
    
    faculty = []
    for user in faculty_users:
        faculty.append({
            'username': user.username,
            'name': user.name
        })
    
    session.close()
    return faculty

def get_faculty_publications(faculty_username):
    """Get publications for a specific faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    if not faculty:
        session.close()
        return []
    
    # Get publications
    publications = session.query(Publication).filter(Publication.faculty_id == faculty.id).all()
    
    # Convert to list of dictionaries
    result = []
    for pub in publications:
        result.append({
            'id': pub.id,
            'faculty_username': faculty_username,
            'title': pub.title,
            'journal': pub.journal,
            'year': pub.year,
            'doi': pub.doi
        })
    
    session.close()
    return result

def add_publication(faculty_username, title, journal, year, doi):
    """Add a new publication for a faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    if not faculty:
        session.close()
        return None
    
    # Create new publication
    new_pub = Publication(
        faculty_id=faculty.id,
        title=title,
        journal=journal,
        year=year,
        doi=doi
    )
    
    session.add(new_pub)
    session.commit()
    pub_id = new_pub.id
    session.close()
    
    return pub_id

def update_publication(pub_id, title, journal, year, doi):
    """Update an existing publication"""
    session = get_db_session()
    
    # Get the publication
    pub = session.query(Publication).filter(Publication.id == pub_id).first()
    if not pub:
        session.close()
        return False
    
    # Update publication
    pub.title = title
    pub.journal = journal
    pub.year = year
    pub.doi = doi
    
    session.commit()
    session.close()
    
    return True

def delete_publication(pub_id):
    """Delete a publication"""
    session = get_db_session()
    
    # Get the publication
    pub = session.query(Publication).filter(Publication.id == pub_id).first()
    if not pub:
        session.close()
        return False
    
    # Delete publication
    session.delete(pub)
    session.commit()
    session.close()
    
    return True

def get_faculty_experiences(faculty_username):
    """Get experiences for a specific faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    if not faculty:
        session.close()
        return []
    
    # Get experiences
    experiences = session.query(Experience).filter(Experience.faculty_id == faculty.id).all()
    
    # Convert to list of dictionaries
    result = []
    for exp in experiences:
        result.append({
            'id': exp.id,
            'faculty_username': faculty_username,
            'institution': exp.institution,
            'role': exp.role,
            'duration': exp.duration,
            'description': exp.description
        })
    
    session.close()
    return result

def add_experience(faculty_username, institution, role, duration, description):
    """Add a new experience for a faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    if not faculty:
        session.close()
        return None
    
    # Create new experience
    new_exp = Experience(
        faculty_id=faculty.id,
        institution=institution,
        role=role,
        duration=duration,
        description=description
    )
    
    session.add(new_exp)
    session.commit()
    exp_id = new_exp.id
    session.close()
    
    return exp_id

def update_experience(exp_id, institution, role, duration, description):
    """Update an existing experience"""
    session = get_db_session()
    
    # Get the experience
    exp = session.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        session.close()
        return False
    
    # Update experience
    exp.institution = institution
    exp.role = role
    exp.duration = duration
    exp.description = description
    
    session.commit()
    session.close()
    
    return True

def delete_experience(exp_id):
    """Delete an experience"""
    session = get_db_session()
    
    # Get the experience
    exp = session.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        session.close()
        return False
    
    # Delete experience
    session.delete(exp)
    session.commit()
    session.close()
    
    return True

def get_faculty_feedback(faculty_username):
    """Get feedback for a specific faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    if not faculty:
        session.close()
        return []
    
    # Get feedback
    feedbacks = session.query(Feedback).filter(Feedback.faculty_id == faculty.id).all()
    
    # Convert to list of dictionaries
    result = []
    for feedback in feedbacks:
        # Get related users
        student_username = None
        if feedback.student_id:
            student = get_user_by_id(feedback.student_id)
            student_username = student.username if student else None
            
        dean_username = None
        if feedback.dean_id:
            dean = get_user_by_id(feedback.dean_id)
            dean_username = dean.username if dean else None
        
        result.append({
            'id': feedback.id,
            'faculty_username': faculty_username,
            'student_username': student_username,
            'dean_username': dean_username,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'semester': feedback.semester,
            'timestamp': feedback.timestamp.strftime("%Y-%m-%d %H:%M:%S") if feedback.timestamp else ""
        })
    
    session.close()
    return result

def has_given_feedback(student_username, faculty_username, semester):
    """Check if a student has already given feedback to a faculty in the current semester"""
    session = get_db_session()
    
    # Get the student and faculty users
    student = get_user_by_username(student_username)
    faculty = get_user_by_username(faculty_username)
    
    if not student or not faculty:
        session.close()
        return False
    
    # Check if feedback exists
    feedback_exists = session.query(Feedback).filter(
        Feedback.student_id == student.id,
        Feedback.faculty_id == faculty.id,
        Feedback.semester == semester
    ).first() is not None
    
    session.close()
    return feedback_exists

def add_feedback(from_username, from_role, faculty_username, rating, comment, semester):
    """Add feedback for a faculty member"""
    session = get_db_session()
    
    # Get the faculty user
    faculty = get_user_by_username(faculty_username)
    from_user = get_user_by_username(from_username)
    
    if not faculty or not from_user:
        session.close()
        return False, "User not found."
    
    # For students, check if already given feedback this semester
    if from_role == 'student' and has_given_feedback(from_username, faculty_username, semester):
        session.close()
        return False, "You have already submitted feedback for this faculty this semester."
    
    # Create feedback object
    new_feedback = Feedback(
        faculty_id=faculty.id,
        student_id=from_user.id if from_role == 'student' else None,
        dean_id=from_user.id if from_role == 'dean' else None,
        rating=rating,
        comment=comment,
        semester=semester
    )
    
    session.add(new_feedback)
    session.commit()
    
    session.close()
    return True, "Feedback submitted successfully."

def get_feedback_summary(faculty_username):
    """Get average rating and comments for a faculty member"""
    feedback = get_faculty_feedback(faculty_username)
    
    if not feedback:
        return {
            'avg_rating': 0,
            'student_count': 0,
            'dean_count': 0,
            'feedback': []
        }
    
    ratings = [f['rating'] for f in feedback]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    student_count = sum(1 for f in feedback if f['student_username'] is not None)
    dean_count = sum(1 for f in feedback if f['dean_username'] is not None)
    
    return {
        'avg_rating': round(avg_rating, 1),
        'student_count': student_count,
        'dean_count': dean_count,
        'feedback': feedback
    }

def get_current_semester():
    """Get the current academic semester"""
    return st.session_state.current_semester
