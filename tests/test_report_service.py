# tests/test_report_service.py
import pytest
import os
from datetime import datetime
from src.services.report_service import ReportService
from src.models.bug import Bug, Status, Severity, Priority

@pytest.fixture
def report_service():
    return ReportService()

@pytest.fixture
def sample_bugs():
    return [
        Bug(
            id="1",
            title="Bug 1",
            description="Test Description",
            severity=Severity.HIGH,
            priority=Priority.HIGH,
            status=Status.OPEN,
            assigned_to="john.doe",
            created_by="jane.doe",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            steps_to_reproduce="Test steps",
            expected_result="Expected",
            actual_result="Actual"
        )
    ]

def test_generate_excel_report(report_service, sample_bugs, tmp_path):
    # Create a temporary filename
    filename = "test_report"
    
    # Generate the report
    filepath = report_service.generate_excel_report(sample_bugs, filename)
    
    # Verify file exists and is not empty
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0
    
    # Cleanup
    os.remove(filepath)
    
    # Verify the reports directory still exists
    assert os.path.exists(report_service.reports_dir)

def test_generate_pdf_report(report_service, sample_bugs, tmp_path):
    # Create a temporary filename
    filename = "test_report"
    
    # Generate the report
    filepath = report_service.generate_pdf_report(sample_bugs, filename)
    
    # Verify file exists and is not empty
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 0
    
    # Cleanup
    os.remove(filepath)
    
    # Verify the reports directory still exists
    assert os.path.exists(report_service.reports_dir)

@pytest.fixture(autouse=True)
def cleanup():
    # Setup: ensure reports directory exists
    reports_dir = os.path.join(os.getcwd(), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    yield
    
    # Cleanup: remove any test files but keep the directory
    for file in os.listdir(reports_dir):
        if file.startswith('test_'):
            os.remove(os.path.join(reports_dir, file))  