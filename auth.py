import streamlit as st
from db_setup import get_db_session, User

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current authenticated user"""
    if not is_authenticated():
        return None
    
    session = get_db_session()
    username = st.session_state.username
    user = session.query(User).filter(User.username == username).first()
    
    if not user:
        session.close()
        return None
    
    result = {
        'username': user.username,
        'name': user.name,
        'role': user.role
    }
    
    session.close()
    return result

def authenticate_user(username, password, role):
    """Authenticate a user with username, password and role"""
    session = get_db_session()
    user = session.query(User).filter(User.username == username).first()
    
    if user and user.password == password and user.role == role:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.user_role = role
        session.close()
        return True
    
    session.close()
    return False

def register_user(username, password, name, role):
    """Register a new user"""
    session = get_db_session()
    
    # Check if username already exists
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        session.close()
        return False
    
    # Create new user
    new_user = User(
        username=username,
        password=password,
        name=name,
        role=role
    )
    
    session.add(new_user)
    session.commit()
    session.close()
    
    return True

def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.current_menu = "Login"
