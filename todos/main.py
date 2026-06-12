from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated
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
