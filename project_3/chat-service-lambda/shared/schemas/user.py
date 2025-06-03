# === shared/schemas/user.py ===

"""Pydantic schemas related to user data.

Includes response models for user registration and user search results.
"""

from pydantic import BaseModel, Field


class UserRegisterOut(BaseModel):
    """
    Response schema for confirming successful user registration.

    Returned after completing the registration process.
    """

    message: str = Field(..., description="Confirmation message indicating registration was successful")

    class Config:
        from_attributes = True


class UserSearchOut(BaseModel):
    """
    Minimal user data returned in user search results.

    Used in endpoints that return a list of users matching search criteria.
    """

    sub: str = Field(..., description="Cognito subject (sub) identifier of the user")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")

    class Config:
        from_attributes = True
