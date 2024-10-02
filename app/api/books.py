from app.api import crud
from fastapi import APIRouter, HTTPException, Path
from datetime import datetime as dt
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.db import engine
from app.api.models import books,reviews
from http import HTTPStatus
from typing import List
import uuid
from app.api.schemas import book, review

router = APIRouter()
#create an async session object for CRUD
session = async_sessionmaker(bind=engine, expire_on_commit=False)

@router.post("/", response_model= book)
async def add_book(book: book):
    new_book = books(
        id = str(uuid.uuid4()),
        year_published = book.year_published,
        title = book.title,
        author = book.author,
        genre = book.genre,
        summary = book.summary
    )
    return await crud.add_book(new_book, session)

@router.get("/")
async def read_all_books():
    return await crud.get_all(session)

@router.get("/{id}/", response_model=book)
async def read_note(id: str):
    book = await crud.get_book_by_id(id, session)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book


@router.put("/{id}/", response_model=book)
async def update_book_details(id: str, book: book):  
    book = await crud.update_book_details(id, book, session)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return book


# Delete a book
@router.delete("/{id}/", response_model=None)
async def delete_book_by_id(id: str):
    book = await crud.get_book_by_id(id, session)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return await crud.delete_book(book, session)


#Add review to a book
@router.post("/{id}/reviews", response_model= review)
async def add_review_for_a_book(review: review):
    new_review = reviews(
        id = str(uuid.uuid4()),
        user_id = review.user_id,
        rating = review.rating,
        review_text = review.review_text,
        book_id = review.book_id
    )
    return await crud.add_review_for_book(new_review, session)


# Retrieve all reviews for a book
@router.get("/{id}/reviews", response_model=None)
async def read_all_reviews_by_book_id(book_id: str):
    review = await crud.get_book_reviews(book_id, session)
    if not review:
        raise HTTPException(status_code=404, detail="book not found")
    return review

@router.get("/{id}/summary", response_model=None)
async def get_book_summary_and_aggregated_rating(id: str):
    book = await crud.get_book_by_id(id, session)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return await crud.get_summary_and_aggregated_rating(book, id, session)

#Generate summary for a book content
@router.post("/generate_summary", response_model= None)
async def generate_summary(book_content, book_id):
    global book
    book_details = await crud.get_book_by_id(book_id, session)
    book_title = book_details.title
    summary =  await crud.generate_summary(book_content, book_title)
    updated_book = book(
        author = "",
        title = "",
        summary = summary,
        genre= "",
        year_published = 0)
    await crud.update_book_details(book_id, updated_book, session)
    return summary

# Generate book recommendations based on user preferences
@router.post("/recommendations", response_model= None)
async def recommendations(user_preferences):
    return await crud.recommendations(user_preferences)