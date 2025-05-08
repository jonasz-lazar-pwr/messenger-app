# api/schemas/user.py

from pydantic import BaseModel, Field, EmailStr


class UserRegisterIn(BaseModel):
    """Payload for registering a new user."""
    sub: str = Field(..., description="Cognito user sub (unique identifier)")
    email: EmailStr = Field(..., description="User's email address")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")


class UserRegisterOut(BaseModel):
    """Response confirming user registration."""
    message: str = Field(..., description="Confirmation message")


class UserSearchOut(BaseModel):
    """Minimal user data returned in user search results."""
    sub: str = Field(..., description="Cognito sub of the user")
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")

    class Config:
        from_attributes = True
