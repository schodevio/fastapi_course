from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from starlette import status

import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoCreateDTO(BaseModel):
    title: str = Field(..., min_length=3, example="Buy groceries")
    description: str = Field(..., max_length=100, example="Milk, Bread, Eggs")
    priority: int = Field(..., ge=1, le=5, example=3)
    completed: bool = Field(..., example=False)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(models.Todo).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, db: db_dependency):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(params: TodoCreateDTO, db: db_dependency):
    db_todo = models.Todo(
        title=params.title,
        description=params.description,
        priority=params.priority,
        completed=params.completed
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, params: TodoCreateDTO, db: db_dependency):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    todo.title = params.title
    todo.description = params.description
    todo.priority = params.priority
    todo.completed = params.completed

    db.commit()
    db.refresh(todo)

    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: db_dependency):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()
