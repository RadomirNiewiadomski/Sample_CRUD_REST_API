from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from .database import Base


class Parent(Base):
    """
    ORM model representing the 'parents' table in the database.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Name of the parent.
        age (int): Age of the parent.
        email (str): Email address of the parent, must be unique.
        address (str): Address of the parent.
        children (List[Child]): List of Child objects related to this parent (one-to-many relationship).
    """

    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(TINYINT(unsigned=True), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    address = Column(String(255), nullable=False)

    children = relationship(
        "Child", back_populates="parent", cascade="all, delete-orphan"
    )


class Child(Base):
    """
    ORM model representing the 'children' table in the database.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Name of the child.
        age (int): Age of the child.
        parent_id (int): Foreign key referencing the 'parents' table.
        hobby (str): Hobby of the child.
        parent (Parent): The Parent object that this child is related to (many-to-one relationship).
    """

    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(TINYINT(unsigned=True), nullable=False)
    parent_id = Column(
        Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
    hobby = Column(String(100))

    parent = relationship("Parent", back_populates="children")
