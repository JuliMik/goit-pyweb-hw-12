from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from app.schemas import ContactResponse, ContactCreate
from app.repository import contacts
from app.auth.security import get_current_user
from app.models import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Пошук контактів
@router.get("/search", response_model=List[ContactResponse])
def search_contacts(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return contacts.search_contacts(first_name, last_name, email, db, current_user)


# Створення контакту
@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
        contact: ContactCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return contacts.create_contact(db, contact, current_user)


# Отримання одного контакту
@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    contact = contacts.get_contact_by_id(contact_id, db, current_user)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Отримання всіх контактів
@router.get("/", response_model=List[ContactResponse])
def get_contacts(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return contacts.get_all_contacts(db, current_user)


# Оновлення контакту
@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
        contact_id: int,
        contact: ContactCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    updated = contacts.update_contact(contact_id, contact, db, current_user)
    if updated is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated


# Видалення контакту
@router.delete("/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_contact = contacts.get_contact_by_id(contact_id, db, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(db_contact)
    db.commit()
    return db_contact


# Отримання контактів з днями народження на найближчі 7 днів
@router.get("/birthdays/", response_model=List[schemas.ContactResponse])
def upcoming_birthdays(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return contacts.get_upcoming_birthdays(db, current_user)
