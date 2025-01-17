# pages/analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import DatabaseManager
from src.services.bug_service import BugService
from src.services.analytics_service import AnalyticsService

st.set_page_config(page_title="Bug Analytics", page_icon="📊", layout="wide")

# Initialize services
db_manager = DatabaseManager()
bug_service = BugService(db_manager)
analytics_service = AnalyticsService()

st.title("Bug Analytics Dashboard")

# Get all bugs and calculate statistics
all_bugs = bug_service.get_all_bugs()
stats = analytics_service.get_bug_statistics(all_bugs)

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Bugs", stats['total_bugs'])
with col2:
    st.metric("Open Bugs", stats['open_bugs'])
with col3:
    st.metric("Resolved Bugs", stats['resolved_bugs'])

# Create interactive charts using plotly
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bugs by Status")
    status_data = pd.DataFrame(
        list(stats['status_distribution'].items()),
        columns=['Status', 'Count']
    )
    if not status_data.empty:
        fig = px.pie(status_data, values='Count', names='Status', title='Bug Distribution by Status')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No status data available")

with col2:
    st.subheader("Bugs by Severity")
    severity_data = pd.DataFrame(
        list(stats['severity_distribution'].items()),
        columns=['Severity', 'Count']
    )
    if not severity_data.empty:
        fig = px.bar(severity_data, x='Severity', y='Count', title='Bugs by Severity Level')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No severity data available")

# Show trend over time
if all_bugs:
    st.subheader("Bug Creation Trend")
    dates = [bug.created_at.date() for bug in all_bugs]
    date_counts = pd.Series(dates).value_counts().sort_index()
    trend_data = pd.DataFrame({
        'Date': date_counts.index,
        'Count': date_counts.values
    })
    fig = px.line(trend_data, x='Date', y='Count', title='Bug Creation Trend Over Time')
    st.plotly_chart(fig, use_container_width=True)

# Priority Analysis
st.subheader("Priority vs Severity Analysis")
if all_bugs:
    priority_severity = pd.DataFrame([
        {'Priority': bug.priority.value, 'Severity': bug.severity.value}
        for bug in all_bugs
    ])
    pivot_table = pd.crosstab(priority_severity['Priority'], priority_severity['Severity'])
    fig = px.imshow(pivot_table, 
                    labels=dict(x="Severity", y="Priority", color="Count"),
                    title="Priority vs Severity Heatmap")
    st.plotly_chart(fig, use_container_width=True)