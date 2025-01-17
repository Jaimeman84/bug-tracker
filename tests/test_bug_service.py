# tests/test_bug_service.py
import pytest
from datetime import datetime
import time
from src.models.bug import Bug, Status, Severity, Priority
from src.services.bug_service import BugService

# Mock Database Manager
class MockDBManager:
    def __init__(self):
        self.bugs = {}

    def save_bug(self, bug):
        self.bugs[bug.id] = bug
        return bug

    def get_bug(self, bug_id):
        return self.bugs.get(bug_id)

    def update_bug(self, bug):
        self.bugs[bug.id] = bug
        return bug

# Fixtures
@pytest.fixture
def db_manager():
    return MockDBManager()

@pytest.fixture
def bug_service(db_manager):
    return BugService(db_manager)

@pytest.fixture
def sample_bug_data():
    return {
        'title': 'Test Bug',
        'description': 'Test Description',
        'severity': 'HIGH',
        'priority': 'MEDIUM',
        'assigned_to': 'john.doe',
        'created_by': 'jane.doe',
        'steps_to_reproduce': 'Test steps',
        'expected_result': 'Expected',
        'actual_result': 'Actual'
    }

# Tests
def test_create_bug(bug_service, sample_bug_data):
    bug = bug_service.create_bug(sample_bug_data)
    
    assert bug.id is not None
    assert bug.title == sample_bug_data['title']
    assert bug.severity == Severity.HIGH
    assert bug.status == Status.OPEN

def test_update_bug(bug_service, sample_bug_data):
    # First create a bug
    bug = bug_service.create_bug(sample_bug_data)
    
    # Add a small delay to ensure time difference
    time.sleep(0.001)
    
    # Update the bug
    update_data = {
        'status': Status.IN_PROGRESS,
        'assigned_to': 'alice.smith'
    }
    
    updated_bug = bug_service.update_bug(bug.id, update_data)
    
    # Verify the updates
    assert updated_bug.status == Status.IN_PROGRESS
    assert updated_bug.assigned_to == 'alice.smith'
    
    # Verify timestamps are different and in correct order
    assert updated_bug.updated_at > updated_bug.created_at
    assert (updated_bug.updated_at - updated_bug.created_at).total_seconds() > 0

def test_update_nonexistent_bug(bug_service):
    update_data = {
        'status': Status.IN_PROGRESS
    }
    result = bug_service.update_bug('nonexistent-id', update_data)
    assert result is None