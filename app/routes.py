from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from typing import List

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.post(
    "/parents/", response_model=schemas.Parent, status_code=status.HTTP_201_CREATED
)
def create_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    """
    Create a new Parent.

    Args:
        parent (schemas.ParentCreate): Data for creating a new Parent.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Parent: The created Parent object.
    """

    return crud.create_parent(db=db, parent=parent)


@router.post(
    "/children/", response_model=schemas.Child, status_code=status.HTTP_201_CREATED
)
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db)):
    """
    Create a new Child.

    Args:
        child (schemas.ChildCreate): Data for creating a new Child.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Child: The created Child object.
    """

    return crud.create_child(db=db, child=child)


@router.get("/parents/", response_model=List[schemas.Parent])
def read_parents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of Parent records along with their corresponding children.

    Args:
        skip (int, optional): Number of records to skip.
        limit (int, optional): Maximum number of records to return.
        db (Session, optional): SQLAlchemy session.

    Returns:
        list[schemas.Parent]: A list of Parent objects with their children.
    """

    return crud.get_parents(db=db, skip=skip, limit=limit)


@router.get("/children/", response_model=List[schemas.Child])
def read_children(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of Child records along.

    Args:
        skip (int, optional): Number of records to skip.
        limit (int, optional): Maximum number of records to return.
        db (Session, optional): SQLAlchemy session.

    Returns:
        list[schemas.Parent]: A list of Child objects.
    """

    return crud.get_children(db=db, skip=skip, limit=limit)


@router.get("/parents/{parent_id}", response_model=schemas.Parent)
def read_specific_parent(parent_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the specific Parent along with its related Children.

    Args:
        parent_id (int): ID of the Parent to retrieve.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Parent: The specific Parent object with related Children.
    """
    return crud.get_specific_parent(db=db, parent_id=parent_id)


@router.get("/children/{child_id}", response_model=schemas.Child)
def read_specific_child(child_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the specific Child.

    Args:
        child_id (int): ID of the Child to retrieve.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Child: The specific Child object.
    """
    return crud.get_specific_child(db=db, child_id=child_id)


@router.put("/parents/{parent_id}", response_model=schemas.Parent)
def update_parent(
    parent_id: int, parent: schemas.ParentUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing Parent.

    Args:
        parent_id (int): ID of the Parent to update.
        parent (schemas.ParentUpdate): Updated data for the Parent.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Parent: The updated Parent object.
    """
    return crud.update_parent(db=db, parent_id=parent_id, parent_update=parent)


@router.put("/children/{child_id}", response_model=schemas.Child)
def update_child(
    child_id: int, child: schemas.ChildUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing Child.

    Args:
        child_id (int): ID of the Child to update.
        child (schemas.ChildUpdate): Updated data for the Child.
        db (Session, optional): SQLAlchemy session.

    Returns:
        schemas.Child: The updated Child object.
    """
    return crud.update_child(db=db, child_id=child_id, child_update=child)


@router.delete("/parents/{parent_id}", response_model=dict)
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing Parent.

    Args:
        parent_id (int): ID of the Parent to delete.
        db (Session, optional): SQLAlchemy session.

    Returns:
        dict: Success message.
    """
    return crud.delete_parent(db=db, parent_id=parent_id)


@router.delete("/children/{child_id}", response_model=dict)
def delete_child(child_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing Child.

    Args:
        child_id (int): ID of the Child to delete.
        db (Session, optional): SQLAlchemy session.

    Returns:
        dict: Success message.
    """
    return crud.delete_child(db=db, child_id=child_id)
