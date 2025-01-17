# src/services/bug_service.py
from datetime import datetime
import uuid
import time
from typing import List, Optional
from ..models.bug import Bug, Status, Severity, Priority

class BugService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_bug(self, bug_data: dict) -> Bug:
        bug_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        bug = Bug(
            id=bug_id,
            title=bug_data['title'],
            description=bug_data['description'],
            severity=Severity[bug_data['severity']],
            priority=Priority[bug_data['priority']],
            status=Status.OPEN,
            assigned_to=bug_data['assigned_to'],
            created_by=bug_data['created_by'],
            created_at=current_time,
            updated_at=current_time,
            steps_to_reproduce=bug_data['steps_to_reproduce'],
            expected_result=bug_data['expected_result'],
            actual_result=bug_data['actual_result']
        )
        
        return self.db_manager.save_bug(bug)

    def get_bug(self, bug_id: str) -> Optional[Bug]:
        """Retrieve a specific bug by ID"""
        return self.db_manager.get_bug(bug_id)

    def update_bug(self, bug_id: str, update_data: dict) -> Optional[Bug]:
        bug = self.db_manager.get_bug(bug_id)
        if not bug:
            return None
            
        for key, value in update_data.items():
            if hasattr(bug, key):
                setattr(bug, key, value)
        
        time.sleep(0.001)  # Ensure time difference for updates
        bug.updated_at = datetime.now()
        return self.db_manager.update_bug(bug)

    def get_all_bugs(self) -> List[Bug]:
        """Retrieve all bugs"""
        return self.db_manager.get_all_bugs()

    def get_bugs_by_status(self, status: Status) -> List[Bug]:
        """Retrieve all bugs with a specific status"""
        return self.db_manager.get_bugs_by_status(status)

    def get_filtered_bugs(self, status_filter: List[str] = None, 
                         severity_filter: List[str] = None,
                         priority_filter: List[str] = None) -> List[Bug]:
        """Retrieve bugs with specified filters"""
        all_bugs = self.get_all_bugs()
        filtered_bugs = all_bugs

        if status_filter:
            filtered_bugs = [bug for bug in filtered_bugs 
                           if bug.status.value in status_filter]

        if severity_filter:
            filtered_bugs = [bug for bug in filtered_bugs 
                           if bug.severity.value in severity_filter]

        if priority_filter:
            filtered_bugs = [bug for bug in filtered_bugs 
                           if bug.priority.value in priority_filter]

        return filtered_bugs

    def delete_bug(self, bug_id: str) -> bool:
        """Delete a bug by ID"""
        return self.db_manager.delete_bug(bug_id)