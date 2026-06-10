from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Fiction"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Fiction"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopian"
    },
]


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/books")
async def read_books(author: str = None, category: str = None):
    output = []

    for book in BOOKS:
        if author and book["author"] != author:
            continue
        if category and book["category"] != category:
            continue
        output.append(book)

    return output


@app.post("/books")
async def create_book(book: dict = Body(...)):
    new_id = max(book["id"] for book in BOOKS) + 1
    book["id"] = new_id
    BOOKS.append(book)

    return book


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book

    return {"error": "Book not found"}


@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: dict = Body(...)):
    for book in BOOKS:
        if book["id"] == book_id:
            book.update(updated_book)
            return book

    return {"error": "Book not found"}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return {"message": "Book deleted"}

    return {"error": "Book not found"}
