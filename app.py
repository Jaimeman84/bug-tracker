# app.py
import streamlit as st
import pandas as pd
from src.services.bug_service import BugService
from src.services.report_service import ReportService
from src.services.analytics_service import AnalyticsService
from src.database.db_manager import DatabaseManager
from src.models.bug import Status, Severity, Priority

def main():
    st.set_page_config(
        page_title="Bug Tracker",
        page_icon="🐛",
        layout="wide"
    )

    # Initialize services
    db_manager = DatabaseManager()
    bug_service = BugService(db_manager)
    report_service = ReportService()
    analytics_service = AnalyticsService()

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Create Bug", "Bug List", "Reports"]
    )

    if page == "Dashboard":
        show_dashboard(bug_service, analytics_service)
    elif page == "Create Bug":
        show_create_bug(bug_service)
    elif page == "Bug List":
        show_bug_list(bug_service)
    else:
        show_reports(bug_service, report_service)

def show_dashboard(bug_service, analytics_service):
    st.title("Bug Tracker Dashboard")
    
    # Get all bugs and calculate statistics
    all_bugs = bug_service.get_all_bugs()
    stats = analytics_service.get_bug_statistics(all_bugs)
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Bugs", stats['total_bugs'])
    with col2:
        st.metric("Open Bugs", stats['open_bugs'])
    with col3:
        st.metric("Resolved Bugs", stats['resolved_bugs'])
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bugs by Status")
        status_data = pd.DataFrame(
            list(stats['status_distribution'].items()),
            columns=['Status', 'Count']
        )
        if not status_data.empty:
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("No status data available")
    
    with col2:
        st.subheader("Bugs by Severity")
        severity_data = pd.DataFrame(
            list(stats['severity_distribution'].items()),
            columns=['Severity', 'Count']
        )
        if not severity_data.empty:
            st.bar_chart(severity_data.set_index('Severity'))
        else:
            st.info("No severity data available")

def show_create_bug(bug_service):
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
                return
                
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
            except Exception as e:
                st.error(f"Error creating bug: {str(e)}")

def show_bug_list(bug_service):
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
    else:
        st.info("No bugs found matching the criteria.")

def show_reports(bug_service, report_service):
    st.title("Generate Reports")
    
    report_type = st.radio("Report Format", ["Excel", "PDF"])
    
    # Add date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    if st.button("Generate Report"):
        bugs = bug_service.get_all_bugs()
        
        # Filter bugs by date if specified
        if start_date and end_date:
            bugs = [bug for bug in bugs 
                   if start_date <= bug.created_at.date() <= end_date]
        
        if not bugs:
            st.warning("No bugs found in the selected date range.")
            return
            
        try:
            if report_type == "Excel":
                filepath = report_service.generate_excel_report(bugs, "bug_report")
                st.success(f"Excel report generated: {filepath}")
            else:
                filepath = report_service.generate_pdf_report(bugs, "bug_report")
                st.success(f"PDF report generated: {filepath}")
                
            # Add download button
            with open(filepath, 'rb') as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=f"bug_report.{'xlsx' if report_type == 'Excel' else 'pdf'}",
                    mime="application/octet-stream"
                )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    main()