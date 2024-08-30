import json

import redis

import os

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from typing import List

from . import crud, schemas
from .database import get_db


router = APIRouter()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)


def delete_keys_by_pattern(pattern: str):
    """Helper function for invalidating cache."""
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)


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
    new_parent = crud.create_parent(db=db, parent=parent)

    # Invalidate cache
    delete_keys_by_pattern("parents:*")

    return new_parent


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
    new_child = crud.create_child(db=db, child=child)

    # Invalidate cache
    delete_keys_by_pattern("children:*")
    delete_keys_by_pattern("parents:*")

    return new_child


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
    cache_key = f"parents:{skip}:{limit}"
    cached_parents = redis_client.get(cache_key)

    if cached_parents:
        return json.loads(cached_parents)

    parents = crud.get_parents(db=db, skip=skip, limit=limit)
    # Convert SQLAlchemy models to Pydantic schemas for serialization
    parents_data = [
        schemas.Parent.model_validate(parent).model_dump() for parent in parents
    ]
    redis_client.set(
        cache_key, json.dumps(parents_data), ex=60 * 5
    )  # Cache for 5 minutes

    return parents


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
    cache_key = f"children:{skip}:{limit}"
    cached_children = redis_client.get(cache_key)

    if cached_children:
        return json.loads(cached_children)

    children = crud.get_children(db=db, skip=skip, limit=limit)
    # Convert SQLAlchemy models to Pydantic schemas for serialization
    children_serialized = [
        schemas.Child.model_validate(child).model_dump() for child in children
    ]
    redis_client.set(
        cache_key, json.dumps(children_serialized), ex=60 * 5
    )  # Cache for 5 minutes

    return children


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
    specific_parent = crud.get_specific_parent(db=db, parent_id=parent_id)

    return specific_parent


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
    specific_child = crud.get_specific_child(db=db, child_id=child_id)

    return specific_child


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
    updated_parent = crud.update_parent(
        db=db, parent_id=parent_id, parent_update=parent
    )

    # Invalidate the cache for this specific parent
    delete_keys_by_pattern("parents:*")

    return updated_parent


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
    updated_child = crud.update_child(db=db, child_id=child_id, child_update=child)

    # Invalidate the cache for this specific parent
    delete_keys_by_pattern("children:*")
    delete_keys_by_pattern("parents:*")

    return updated_child


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
    delete_message = crud.delete_parent(db=db, parent_id=parent_id)

    # Invalidate the list cache
    delete_keys_by_pattern("children:*")
    delete_keys_by_pattern("parents:*")

    return delete_message


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
    delete_message = crud.delete_child(db=db, child_id=child_id)

    # Invalidate the list cache
    delete_keys_by_pattern("children:*")
    delete_keys_by_pattern("parents:*")

    return delete_message
