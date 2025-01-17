# src/models/bug.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Severity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

@dataclass
class Bug:
    id: str
    title: str
    description: str
    severity: Severity
    priority: Priority
    status: Status
    assigned_to: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    steps_to_reproduce: str
    expected_result: str
    actual_result: str
    