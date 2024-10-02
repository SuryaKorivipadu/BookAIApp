from app.api.models import books, reviews
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, func
from app.api.schemas import book, review
import requests
import urllib
import json
import aiofiles

url = "http://localhost:11434/api/generate"

async def get_all(async_session: async_sessionmaker[AsyncSession]):
    """
    Get all entries from books table
    """
    async with async_session() as session:
        statement = select(books)
        result = await session.execute(statement)
        return result.mappings().all()

async def add_book(book: book, async_session: async_sessionmaker[AsyncSession]):
    """
    Add a book
    """
    async with async_session() as session:
        session.add(book)
        await session.commit()
    return book

async def get_book_by_id(id: str, async_session: async_sessionmaker[AsyncSession]):
    """
    Get a book details by it's ID
    """
    async with async_session() as session:
        statement = select(books).filter(books.id == id)
        result = await session.execute(statement)
        return result.scalars().one()

async def update_book_details(id: str, book: book, async_session: async_sessionmaker[AsyncSession] ):
    """
    Update book details
    """
    async with async_session() as session:
        statement = select(books).filter(books.id == id)
        result = await session.execute(statement)
        book_details = result.scalars().one()
        if book.year_published != 0:
            book_details.year_published = book.year_published
        if book.title != "":
            book_details.title = book.title
        if book.author != "":
            book_details.author = book.author
        if book.genre != "":
            book_details.genre = book.genre
        if book.summary != "":
            book_details.summary = book.summary
        await session.commit()
    return book


async def delete_book(book: book, async_session: async_sessionmaker[AsyncSession] ):
    """
    Delete a book from books table
    """
    async with async_session() as session:
            await session.delete(book)
            await session.commit()
    return {}

async def add_review_for_book(review: review, async_session: async_sessionmaker[AsyncSession]):
    """
    Add a review for a book
    """
    async with async_session() as session:
        session.add(review)
        await session.commit()
    return review

async def get_book_reviews(book_id: str, async_session: async_sessionmaker[AsyncSession]):
    """
    Get all entries from books table
    """
    async with async_session() as session:
        statement = select(reviews).where(reviews.book_id == book_id)
        result = await session.execute(statement)
        retrieved_reviews = []
        for retrieved_review in result.scalars():
            current_review = {
                "user_id": retrieved_review.user_id,
                "rating": retrieved_review.rating,
                "review_text": retrieved_review.review_text,
                "book_id": retrieved_review.book_id,
                "id": retrieved_review.id
            }
            retrieved_reviews.append(current_review)
        return retrieved_reviews


async def get_summary_and_aggregated_rating(book: book, book_id: str, async_session: async_sessionmaker[AsyncSession]):
    """
    Get book summary and aggregated rating
    """
    async with async_session() as session:
        statement = select(reviews.rating, reviews.book_id)
        result = await session.execute(statement)
        selected_reviews = result.mappings().all()
        current_book_reviews = [row for row in selected_reviews if row.book_id == book_id]
        sum = 0
        for row in current_book_reviews:
            sum += row.rating
    return { "Summary" : book.summary, "Aggregated Rating" : sum}

async def generate_summary(book_content: str, book_title: str):
    """
    Generate summary based on book content and update it in the books table for that book
    """
    prompt = """
    Generate the summary, not exceeding 3 lines, for the following book content:
    Book Title: {Book_Title}
    Book Content: {Book_Content}
    """
    prompt = prompt.format(Book_Title=book_title, Book_Content = book_content)
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    return result.json()['response']

async def recommendations(user_preferences):
    """
    Generate book recommendations based on user preferences
    """
    async with aiofiles.open('available_book_details.txt', 'r') as f:
        available_book_details = await f.read()
    prompt = """
    User Preferences:
    {user_preferences}

    Available book details:
    {available_book_details}
    """
    prompt = prompt.format(user_preferences = user_preferences, available_book_details = available_book_details)
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    return result.json()['response']

