# tests/test_analytics_service.py
import pytest
from src.services.analytics_service import AnalyticsService
from src.models.bug import Bug, Status, Severity, Priority
from datetime import datetime

@pytest.fixture
def analytics_service():
    return AnalyticsService()

@pytest.fixture
def sample_bugs():
    return [
        Bug(
            id="1",
            title="Bug 1",
            description="Test",
            severity=Severity.HIGH,
            priority=Priority.HIGH,
            status=Status.OPEN,
            assigned_to="john.doe",
            created_by="jane.doe",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            steps_to_reproduce="Steps",
            expected_result="Expected",
            actual_result="Actual"
        ),
        Bug(
            id="2",
            title="Bug 2",
            description="Test",
            severity=Severity.MEDIUM,
            priority=Priority.MEDIUM,
            status=Status.RESOLVED,
            assigned_to="john.doe",
            created_by="jane.doe",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            steps_to_reproduce="Steps",
            expected_result="Expected",
            actual_result="Actual"
        )
    ]

def test_get_bug_statistics(analytics_service, sample_bugs):
    stats = analytics_service.get_bug_statistics(sample_bugs)
    
    assert stats['total_bugs'] == 2
    assert stats['open_bugs'] == 1
    assert stats['resolved_bugs'] == 1
    assert stats['status_distribution']['Open'] == 1
    assert stats['severity_distribution']['High'] == 1
    assert stats['priority_distribution']['Medium'] == 1