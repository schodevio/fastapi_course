import time

from fastapi import Body, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    category: str
    published_year: int
    rating: float

    def __init__(self, id: int, title: str, author: str, category: str, published_year: int, rating: float):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.published_year = published_year
        self.rating = rating


class BookCreateDTO(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str
    published_year: int = Field(ge=1990, le=time.localtime().tm_year)
    rating: float = Field(ge=0, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "category": "Classic",
                "published_year": 1925,
                "rating": 4.5
            }
        }
    }


BOOKS = [
    Book(
        id=1,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        category="Fiction",
        published_year=1925,
        rating=4.5
    ),
    Book(
        id=2,
        title="To Kill a Mockingbird",
        author="Harper Lee",
        category="Classic",
        published_year=1960,
        rating=4.8
    )
]


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/books/filter", status_code=status.HTTP_200_OK)
async def books_filter(author: str = None, category: str = None):
    output = []

    for book in BOOKS:
        if author and book.author != author:
            continue
        if category and book.category != category:
            continue
        output.append(book)

    return output


@app.get("/books", status_code=status.HTTP_200_OK)
async def books_index():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def books_show(book_id: int = Path(..., ge=1)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def books_create(params: BookCreateDTO = Body(...)):
    new_id = max(book.id for book in BOOKS) + 1
    new_book = Book(id=new_id, **params.model_dump())

    BOOKS.append(new_book)
    return new_book


@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
async def books_update(
    book_id: int = Path(..., ge=1),
    params: BookCreateDTO = Body(...)
):
    for book in BOOKS:
        if book.id == book_id:
            book.title = params.title
            book.author = params.author
            book.category = params.category
            book.published_year = params.published_year
            book.rating = params.rating

            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def books_delete(book_id: int = Path(..., ge=1)):
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[i]
            return

    raise HTTPException(status_code=404, detail="Book not found")
