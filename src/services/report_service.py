import pandas as pd
from fpdf import FPDF
from typing import List
from ..models.bug import Bug
import os

class ReportService:
    def __init__(self):
        # Ensure reports directory exists
        self.reports_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_excel_report(self, bugs: List[Bug], filename: str) -> str:
        """Generate Excel report of bugs"""
        df = pd.DataFrame([{
            'ID': bug.id,
            'Title': bug.title,
            'Status': bug.status.value,
            'Severity': bug.severity.value,
            'Priority': bug.priority.value,
            'Assigned To': bug.assigned_to,
            'Created At': bug.created_at,
            'Description': bug.description,
            'Steps to Reproduce': bug.steps_to_reproduce,
            'Expected Result': bug.expected_result,
            'Actual Result': bug.actual_result
        } for bug in bugs])
        
        filepath = os.path.join(self.reports_dir, f"{filename}.xlsx")
        df.to_excel(filepath, index=False)
        return filepath

    def generate_pdf_report(self, bugs: List[Bug], filename: str) -> str:
        """Generate PDF report of bugs"""
        pdf = FPDF()
        pdf.add_page()
        
        # Add report content
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Bug Report', 0, 1, 'C')
        
        pdf.set_font('Arial', '', 12)
        for bug in bugs:
            pdf.cell(0, 10, f"Bug ID: {bug.id}", 0, 1)
            pdf.cell(0, 10, f"Title: {bug.title}", 0, 1)
            pdf.cell(0, 10, f"Status: {bug.status.value}", 0, 1)
            pdf.cell(0, 10, f"Severity: {bug.severity.value}", 0, 1)
            pdf.cell(0, 10, f"Priority: {bug.priority.value}", 0, 1)
            pdf.cell(0, 10, f"Assigned To: {bug.assigned_to}", 0, 1)
            pdf.cell(0, 10, '', 0, 1)  # Empty line
            
        filepath = os.path.join(self.reports_dir, f"{filename}.pdf")
        pdf.output(filepath)
        return filepath