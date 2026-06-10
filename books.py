from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
]


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/books")
async def read_books():
    return BOOKS
