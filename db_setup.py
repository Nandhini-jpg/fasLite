import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Use SQLite database
DATABASE_PATH = "faculty_appraisal.db"

# Create SQLAlchemy engine
engine = create_engine(f"sqlite:///{DATABASE_PATH}", connect_args={"check_same_thread": False})

# Create base class for models
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    
    # Relationships
    publications = relationship("Publication", back_populates="faculty", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="faculty", cascade="all, delete-orphan")
    feedbacks_received = relationship("Feedback", back_populates="faculty", foreign_keys="Feedback.faculty_id")
    feedbacks_given_as_student = relationship("Feedback", back_populates="student", foreign_keys="Feedback.student_id")
    feedbacks_given_as_dean = relationship("Feedback", back_populates="dean", foreign_keys="Feedback.dean_id")

class Publication(Base):
    __tablename__ = 'publications'
    
    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    journal = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    doi = Column(String(100))
    
    # Relationships
    faculty = relationship("User", back_populates="publications")

class Experience(Base):
    __tablename__ = 'experiences'
    
    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    institution = Column(String(200), nullable=False)
    role = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)
    description = Column(Text)
    
    # Relationships
    faculty = relationship("User", back_populates="experiences")

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    dean_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    semester = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    faculty = relationship("User", foreign_keys=[faculty_id], back_populates="feedbacks_received")
    student = relationship("User", foreign_keys=[student_id], back_populates="feedbacks_given_as_student")
    dean = relationship("User", foreign_keys=[dean_id], back_populates="feedbacks_given_as_dean")

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

# Function to get a database session
def get_db_session():
    """Get a new database session"""
    return SessionFactory()

# Function to initialize sample data if tables are empty
def initialize_sample_data():
    """Initialize sample data if tables are empty"""
    session = get_db_session()
    
    # Check if users table is empty
    if session.query(User).count() == 0:
        # Create sample users
        sample_users = [
            User(username="john", password="faculty123", name="John Smith", role="faculty"),
            User(username="jane", password="dean123", name="Jane Doe", role="dean"),
            User(username="mike", password="student123", name="Mike Johnson", role="student")
        ]
        session.add_all(sample_users)
        session.commit()
    
    session.close()

# Initialize sample data
initialize_sample_data()