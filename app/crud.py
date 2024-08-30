from fastapi import HTTPException, status

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from . import models, schemas


def create_parent(db: Session, parent: schemas.ParentCreate):
    """
    Create a new Parent record in the database.

    Args:
        db (Session): Database session.
        parent (schemas.ParentCreate): Data for creating a new Parent.

    Returns:
        models.Parent: The newly created Parent object.
    """
    try:
        db_parent = models.Parent(**parent.model_dump())
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
        return db_parent
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Parent with this email already exists."
        )


def create_child(db: Session, child: schemas.ChildCreate):
    """
    Create a new Child record in the database.

    Args:
        db (Session): Database session.
        child (schemas.ChildCreate): Data for creating a new Child.

    Returns:
        models.Child: The newly created Child object.
    """
    db_child = models.Child(**child.model_dump())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child


def get_parents(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of Parent records from the database with optional pagination.

    Args:
        db (Session): Database session.
        skip (int): The number of records to skip for pagination.
        limit (int): The maximum number of records to return.

    Returns:
        List[models.Parent]: A list of Parent objects with their associated children.
    """
    parents = (
        db.query(models.Parent)
        .options(joinedload(models.Parent.children))
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not parents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No parents found"
        )
    return parents


def get_children(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of Child records from the database with optional pagination.

    Args:
        db (Session): Database session.
        skip (int): The number of records to skip for pagination.
        limit (int): The maximum number of records to return.

    Returns:
        List[models.Parent]: A list of Child objects.
    """
    parents = db.query(models.Child).offset(skip).limit(limit).all()
    if not parents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No children found"
        )
    return parents


def get_specific_parent(db: Session, parent_id: int):
    """
    Retrieve the specific Parent record along with its related Children from the database.

    Args:
        db (Session): Database session.
        parent_id (int): ID of the Parent to retrieve.

    Returns:
        models.Parent: The specific Parent object with related Children.
    """
    parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no parent with {parent_id=}",
        )
    return parent


def get_specific_child(db: Session, child_id: int):
    """
    Retrieve the specific Child record from the database.

    Args:
        db (Session): Database session.
        child_id (int): ID of the Child to retrieve.

    Returns:
        models.Child: The specific Child object.
    """
    child = db.query(models.Child).filter(models.Child.id == child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no child with {child_id=}",
        )
    return child


def update_parent(db: Session, parent_id: int, parent_update: schemas.ParentUpdate):
    """
    Update an existing Parent record in the database.

    Args:
        db (Session): Database session.
        parent_id (int): ID of the Parent to update.
        parent_update (schemas.ParentUpdate): Updated data for the Parent.

    Returns:
        models.Parent: The updated Parent object.
    """
    db_parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()

    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    for key, value in parent_update.model_dump().items():
        setattr(db_parent, key, value)

    try:
        db.commit()
        db.refresh(db_parent)
        return db_parent
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Parent with this email already exists."
        )


def update_child(db: Session, child_id: int, child_update: schemas.ChildUpdate):
    """
    Update an existing Child record in the database.

    Args:
        db (Session): Database session.
        child_id (int): ID of the Child to update.
        child_update (schemas.ChildUpdate): Updated data for the Child.

    Returns:
        models.Child: The updated Child object.
    """
    db_child = db.query(models.Child).filter(models.Child.id == child_id).first()

    if not db_child:
        raise HTTPException(status_code=404, detail="Child not found")

    for key, value in child_update.model_dump().items():
        setattr(db_child, key, value)

    db.commit()
    db.refresh(db_child)
    return db_child


def delete_parent(db: Session, parent_id: int):
    """
    Delete an existing Parent record from the database.

    Args:
        db (Session): Database session.
        parent_id (int): ID of the Parent to delete.

    Returns:
        str: Success message if the deletion was successful.
    """
    db_parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()

    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    db.delete(db_parent)
    db.commit()
    return {"detail": f"Parent with ID {parent_id} deleted successfully"}


def delete_child(db: Session, child_id: int):
    """
    Delete an existing Child record from the database.

    Args:
        db (Session): Database session.
        child_id (int): ID of the Child to delete.

    Returns:
        str: Success message if the deletion was successful.
    """
    db_child = db.query(models.Child).filter(models.Child.id == child_id).first()

    if not db_child:
        raise HTTPException(status_code=404, detail="Child not found")

    db.delete(db_child)
    db.commit()
    return {"detail": f"Child with ID {child_id} deleted successfully"}
