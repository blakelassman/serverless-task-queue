from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    type: str

class TaskResponse(BaseModel):
    task_id: str
    type: str
    status: str
    result: Optional[str] = None