# pages/create_bug.py
import streamlit as st
from src.models.bug import Status, Severity, Priority
from src.database.db_manager import DatabaseManager
from src.services.bug_service import BugService

st.set_page_config(page_title="Create Bug", page_icon="🐛", layout="wide")

# Initialize services
db_manager = DatabaseManager()
bug_service = BugService(db_manager)

st.title("Create New Bug")

with st.form("bug_form"):
    title = st.text_input("Bug Title")
    description = st.text_area("Description")
    col1, col2 = st.columns(2)
   
    with col1:
        severity = st.selectbox("Severity", [s.value for s in Severity])
        assigned_to = st.text_input("Assign To")
    
    with col2:
        priority = st.selectbox("Priority", [p.value for p in Priority])
    
    steps = st.text_area("Steps to Reproduce")
    
    col1, col2 = st.columns(2)
    with col1:
        expected = st.text_area("Expected Result")
    with col2:
        actual = st.text_area("Actual Result")
    
    submitted = st.form_submit_button("Create Bug")
    
    if submitted:
        if not title:
            st.error("Bug title is required!")
        else:
            bug_data = {
                'title': title,
                'description': description,
                'severity': severity.upper(),
                'priority': priority.upper(),
                'assigned_to': assigned_to,
                'steps_to_reproduce': steps,
                'expected_result': expected,
                'actual_result': actual,
                'created_by': "current_user"  # In a real app, get from auth
            }
            
            try:
                bug = bug_service.create_bug(bug_data)
                st.success(f"Bug created successfully! ID: {bug.id}")
                st.balloons()
            except Exception as e:
                st.error(f"Error creating bug: {str(e)}")