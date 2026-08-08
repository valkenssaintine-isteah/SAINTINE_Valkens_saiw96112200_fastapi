from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Manager API",
    description="Evaluation finale LOG3550",
    version="1.0.0",
)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = False

class Task(TaskCreate):
    id: int

tasks: List[Task] = [
    Task(
        id=1,
        title="Decouvrir FastAPI",
        description="Creer et tester une API REST",
        completed=False
    )
]

def find_task(task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


@app.get("/", tags=["Accueil"])
def home():
    return {"message": "Bienvenue sur Task Manager API"}

@app.get("/student", tags=["Etudiant"])
def student_information():
    return {
        "name": "SAINTINE Valkens",
        "student_code": "saiw96112200"
    }

@app.get("/tasks/completed", response_model=List[Task], tags=["Tasks"])
def get_completed_tasks():
    return [task for task in tasks if task.completed]

@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tache introuvable",
        )
    return task

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"]
)
def create_task(task_data: TaskCreate):
    new_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(id=new_id, **task_data.model_dump())
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, task_data: TaskCreate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tache introuvable",
        )
    
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    return task

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tache introuvable",
        )
    
    tasks.remove(task)
    return {
        "message": "Tache supprimee avec succes",
        "deleted_task": task
    }