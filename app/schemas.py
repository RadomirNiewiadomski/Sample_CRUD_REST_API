from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ChildBase(BaseModel):
    """
    Base schema for Child.

    Attributes:
        name (str): Name of the child.
        age (int): Age of the child.
        hobby (str): Hobby of the child.
    """

    name: str = Field(
        ..., title="Child's Name", max_length=100, description="The name of the child."
    )
    age: int = Field(
        ...,
        ge=0,
        le=18,
        title="Child's Age",
        description="The age of the child, should be between 0 and 18.",
    )
    hobby: str = Field(
        ...,
        title="Child's Hobby",
        max_length=100,
        description="The hobby of the child.",
    )


class ChildCreate(ChildBase):
    """
    Schema for creating a Child.

    Attributes:
        parent_id (int): Foreign key to the Parent.
    """

    parent_id: int = Field(
        ...,
        title="Parent ID",
        description="The ID of the parent to whom the child belongs.",
    )


class ChildUpdate(BaseModel):
    """
    Schema for updating a Child.

    Attributes:
        name (Optional[str]): Updated name of the child.
        age (Optional[int]): Updated age of the child.
        hobby (Optional[str]): Updated hobby of the child.
    """

    name: Optional[str] = Field(
        None, title="Child's Name", max_length=100, description="The name of the child."
    )
    age: Optional[int] = Field(
        None,
        ge=0,
        le=18,
        title="Child's Age",
        description="The age of the child, should be between 0 and 18.",
    )
    hobby: Optional[str] = Field(
        None,
        title="Child's Hobby",
        max_length=100,
        description="The hobby of the child.",
    )


class Child(ChildBase):
    """
    Schema for returning Child data.

    Attributes:
        id (int): Primary key of the Child.
    """

    id: int = Field(
        ..., title="Child ID", description="The unique identifier of the child."
    )

    class Config:
        from_attributes = True


class ParentBase(BaseModel):
    """
    Base schema for Parent.

    Attributes:
        name (str): Name of the parent.
        age (int): Age of the parent.
        email (str): Email of the parent.
        address (str): Address of the parent.
    """

    name: str = Field(
        ...,
        title="Parent's Name",
        max_length=100,
        description="The name of the parent.",
    )
    age: int = Field(
        ...,
        gt=18,
        title="Parent's Age",
        description="The age of the parent, should be greater than 18.",
    )
    email: EmailStr = Field(
        ..., title="Parent's Email", description="The email address of the parent."
    )
    address: str = Field(
        ...,
        title="Parent's Address",
        max_length=255,
        description="The residential address of the parent.",
    )


class ParentCreate(ParentBase):
    """Schema for creating a Parent."""

    pass


class ParentUpdate(BaseModel):
    """
    Schema for updating a Parent.

    Attributes:
        name (Optional[str]): Updated name of the parent.
        age (Optional[int]): Updated age of the parent.
        email (Optional[EmailStr]): Updated email of the parent.
        address (Optional[str]): Updated address of the parent.
    """

    name: Optional[str] = Field(
        None,
        title="Parent's Name",
        max_length=100,
        description="The name of the parent.",
    )
    age: Optional[int] = Field(
        None,
        gt=18,
        title="Parent's Age",
        description="The age of the parent, should be greater than 18.",
    )
    email: Optional[EmailStr] = Field(
        None, title="Parent's Email", description="The email address of the parent."
    )
    address: Optional[str] = Field(
        None,
        title="Parent's Address",
        max_length=255,
        description="The residential address of the parent.",
    )


class Parent(ParentBase):
    """
    Schema for returning Parent data.

    Attributes:
        id (int): Primary key of the Parent.
        children (List[Child]): List of Child objects related to this parent.
    """

    id: int = Field(
        ..., title="Parent ID", description="The unique identifier of the parent."
    )
    children: list[Child] = Field(
        default=[],
        title="Children",
        description="The list of children belonging to the parent.",
    )

    class Config:
        from_attributes = True
