# pages/bug_list.py
import streamlit as st
import pandas as pd
from src.models.bug import Status, Severity, Priority
from src.database.db_manager import DatabaseManager
from src.services.bug_service import BugService

st.set_page_config(page_title="Bug List", page_icon="📋", layout="wide")

# Initialize services
db_manager = DatabaseManager()
bug_service = BugService(db_manager)

st.title("Bug List")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.multiselect(
        "Status",
        [s.value for s in Status]
    )
with col2:
    severity_filter = st.multiselect(
        "Severity",
        [s.value for s in Severity]
    )
with col3:
    priority_filter = st.multiselect(
        "Priority",
        [p.value for p in Priority]
    )

# Get filtered bugs
bugs = bug_service.get_filtered_bugs(
    status_filter,
    severity_filter,
    priority_filter
)

# Display bugs in a table
if bugs:
    bug_data = [{
        'ID': bug.id,
        'Title': bug.title,
        'Status': bug.status.value,
        'Severity': bug.severity.value,
        'Priority': bug.priority.value,
        'Assigned To': bug.assigned_to,
        'Created At': bug.created_at.strftime('%Y-%m-%d %H:%M')
    } for bug in bugs]
    
    df = pd.DataFrame(bug_data)
    st.dataframe(df)
    
    # Add bug details viewer
    if st.checkbox("View Bug Details"):
        selected_id = st.selectbox(
            "Select Bug ID",
            options=[bug.id for bug in bugs],
            format_func=lambda x: f"{x[:8]} - {next((b.title for b in bugs if b.id == x), '')}"
        )
        
        selected_bug = next((bug for bug in bugs if bug.id == selected_id), None)
        if selected_bug:
            with st.expander("Bug Details", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Description:**\n{selected_bug.description}")
                    st.markdown(f"**Steps to Reproduce:**\n{selected_bug.steps_to_reproduce}")
                with col2:
                    st.markdown(f"**Expected Result:**\n{selected_bug.expected_result}")
                    st.markdown(f"**Actual Result:**\n{selected_bug.actual_result}")
else:
    st.info("No bugs found matching the criteria.")