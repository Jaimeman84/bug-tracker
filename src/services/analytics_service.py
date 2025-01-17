# src/services/analytics_service.py
from collections import Counter
from typing import List, Dict
from ..models.bug import Bug, Status, Severity, Priority

class AnalyticsService:
    def get_bug_statistics(self, bugs: List[Bug]) -> Dict:
        """Calculate bug statistics"""
        return {
            'status_distribution': self._get_status_distribution(bugs),
            'severity_distribution': self._get_severity_distribution(bugs),
            'priority_distribution': self._get_priority_distribution(bugs),
            'total_bugs': len(bugs),
            'open_bugs': len([bug for bug in bugs if bug.status == Status.OPEN]),
            'resolved_bugs': len([bug for bug in bugs if bug.status == Status.RESOLVED])
        }

    def _get_status_distribution(self, bugs: List[Bug]) -> Dict:
        return Counter(bug.status.value for bug in bugs)

    def _get_severity_distribution(self, bugs: List[Bug]) -> Dict:
        return Counter(bug.severity.value for bug in bugs)

    def _get_priority_distribution(self, bugs: List[Bug]) -> Dict:
        return Counter(bug.priority.value for bug in bugs)