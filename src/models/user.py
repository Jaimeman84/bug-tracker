# src/models/user.py
@dataclass
class User:
    id: str
    username: str
    email: str
    role: str