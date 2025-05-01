from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app import db, models

app = FastAPI()
@app.on_event("startup")
def startup_event():
    db.init_db()

# gets incomming POSTs, adds to PostgreSQL, responds with task info
@app.post("/tasks", response_model=models.TaskResponse)
def create_task(task: models.TaskCreate):
    session = db.SessionLocal()
    task_id = str(uuid4())

    db_task = db.Task(
        task_id=task_id,
        type=task.type,
        status="pending"
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    session.close()

    return models.TaskResponse(
        task_id=db_task.task_id,
        type=db_task.type,
        status=db_task.status
    )

# search task by task's id --> returns task id, status, type, and result
@app.get("/tasks/{task_id}", response_model=models.TaskResponse)
def get_task(task_id: str):
    session = db.SessionLocal()
    db_task = session.query(db.Task).filter(db.Task.task_id == task_id).first()
    session.close()

    if not db_task:
        raise HTTPException(status_code=404, detail="Sorry, this task does not exist.")
    
    return models.TaskResponse(
        task_id=db_task.task_id,
        type=db_task.type,
        status=db_task.status,
        result=db_task.result
    )