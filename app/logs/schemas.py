from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    service_name: str
    log_level: str
    message: str
    user_id: int
    document_id: int

class LogCreate(LogBase):
    pass

class Log(LogBase):
    log_id: int
    timestamp: datetime

    class Config:
        from_attributes = True