# src/database/db_manager.py
from sqlalchemy import create_engine, Column, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ..models.bug import Bug, Status, Severity, Priority
import os

Base = declarative_base()

class BugModel(Base):
    __tablename__ = 'bugs'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    severity = Column(Enum(Severity))
    priority = Column(Enum(Priority))
    status = Column(Enum(Status))
    assigned_to = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    steps_to_reproduce = Column(String)
    expected_result = Column(String)
    actual_result = Column(String)

class DatabaseManager:
    def __init__(self):
        db_path = os.getenv('DB_PATH', 'sqlite:///bugs.db')
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_bug(self, bug: Bug) -> Bug:
        bug_model = BugModel(
            id=bug.id,
            title=bug.title,
            description=bug.description,
            severity=bug.severity,
            priority=bug.priority,
            status=bug.status,
            assigned_to=bug.assigned_to,
            created_by=bug.created_by,
            created_at=bug.created_at,
            updated_at=bug.updated_at,
            steps_to_reproduce=bug.steps_to_reproduce,
            expected_result=bug.expected_result,
            actual_result=bug.actual_result
        )
        
        self.session.add(bug_model)
        self.session.commit()
        return bug

    def get_bug(self, bug_id: str) -> Optional[Bug]:
        bug_model = self.session.query(BugModel).filter_by(id=bug_id).first()
        if not bug_model:
            return None
        return self._convert_to_bug(bug_model)

    def update_bug(self, bug: Bug) -> Bug:
        bug_model = self.session.query(BugModel).filter_by(id=bug.id).first()
        if bug_model:
            for key, value in bug.__dict__.items():
                setattr(bug_model, key, value)
            self.session.commit()
        return bug

    def get_all_bugs(self) -> List[Bug]:
        bug_models = self.session.query(BugModel).all()
        return [self._convert_to_bug(model) for model in bug_models]

    def get_bugs_by_status(self, status: Status) -> List[Bug]:
        bug_models = self.session.query(BugModel).filter_by(status=status).all()
        return [self._convert_to_bug(model) for model in bug_models]

    def delete_bug(self, bug_id: str) -> bool:
        bug_model = self.session.query(BugModel).filter_by(id=bug_id).first()
        if bug_model:
            self.session.delete(bug_model)
            self.session.commit()
            return True
        return False

    def _convert_to_bug(self, bug_model: BugModel) -> Bug:
        return Bug(
            id=bug_model.id,
            title=bug_model.title,
            description=bug_model.description,
            severity=bug_model.severity,
            priority=bug_model.priority,
            status=bug_model.status,
            assigned_to=bug_model.assigned_to,
            created_by=bug_model.created_by,
            created_at=bug_model.created_at,
            updated_at=bug_model.updated_at,
            steps_to_reproduce=bug_model.steps_to_reproduce,
            expected_result=bug_model.expected_result,
            actual_result=bug_model.actual_result
        )