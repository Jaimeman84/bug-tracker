# pages/reports.py
import streamlit as st
from src.database.db_manager import DatabaseManager
from src.services.bug_service import BugService
from src.services.report_service import ReportService

st.set_page_config(page_title="Bug Reports", page_icon="📑", layout="wide")

# Initialize services
db_manager = DatabaseManager()
bug_service = BugService(db_manager)
report_service = ReportService()

st.title("Generate Bug Reports")

# Report configuration
report_type = st.radio("Report Format", ["Excel", "PDF"])

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

# Additional filters
with st.expander("Additional Filters"):
    status_filter = st.multiselect("Status", ["Open", "In Progress", "Resolved", "Closed"])
    severity_filter = st.multiselect("Severity", ["Low", "Medium", "High", "Critical"])
    priority_filter = st.multiselect("Priority", ["Low", "Medium", "High"])

if st.button("Generate Report"):
    bugs = bug_service.get_all_bugs()
    
    # Apply date filter
    if start_date and end_date:
        bugs = [bug for bug in bugs 
               if start_date <= bug.created_at.date() <= end_date]
    
    # Apply additional filters
    if status_filter:
        bugs = [bug for bug in bugs if bug.status.value in status_filter]
    if severity_filter:
        bugs = [bug for bug in bugs if bug.severity.value in severity_filter]
    if priority_filter:
        bugs = [bug for bug in bugs if bug.priority.value in priority_filter]
    
    if not bugs:
        st.warning("No bugs found matching the selected criteria.")
    else:
        try:
            if report_type == "Excel":
                filepath = report_service.generate_excel_report(bugs, "bug_report")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                file_extension = "xlsx"
            else:
                filepath = report_service.generate_pdf_report(bugs, "bug_report")
                mime_type = "application/pdf"
                file_extension = "pdf"
            
            st.success(f"Report generated successfully!")
            
            # Add download button
            with open(filepath, 'rb') as file:
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=f"bug_report.{file_extension}",
                    mime=mime_type
                )
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

# Show preview of data being included in report
if st.checkbox("Show Data Preview"):
    bugs = bug_service.get_all_bugs()
    if bugs:
        preview_data = [{
            'ID': bug.id,
            'Title': bug.title,
            'Status': bug.status.value,
            'Severity': bug.severity.value,
            'Priority': bug.priority.value,
            'Created At': bug.created_at.strftime('%Y-%m-%d %H:%M')
        } for bug in bugs]
        st.dataframe(preview_data)