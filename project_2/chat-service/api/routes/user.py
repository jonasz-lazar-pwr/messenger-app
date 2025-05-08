# api/routes/user.py

"""
Routes for user-related operations.

This module provides endpoints to:
- search users by name (first name or last name, case-insensitive),
- register a new user after authentication via Cognito.

Endpoints:
- GET /api/users/search
- POST /api/users/register
"""

from fastapi import APIRouter, status, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.db.deps import get_db
from api.models.user import User
from api.schemas.user import UserSearchOut, UserRegisterOut, UserRegisterIn

# Create a router instance for user-related routes
router = APIRouter()


@router.get(
    "/search",
    response_model=list[UserSearchOut],
    summary="Search users by name",
    description=(
        "Returns users whose first name or last name contains the given query string "
        "(case-insensitive)."
    )
)
async def search_users(
    query: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for users by name (first or last name).

    Performs a case-insensitive search to find users whose first name or last name
    contains the given query string. Returns a list of matching users.

    Args:
        query (str): Search string (min. length 1 character).
        db (AsyncSession): SQLAlchemy async database session (injected).

    Returns:
        list[UserSearchOut]: List of users matching the search criteria.

    Example response:
    ```json
    [
        {
            "sub": "abcd-1234-efgh-5678",
            "first_name": "Alice",
            "last_name": "Wonder"
        },
        {
            "sub": "ijkl-5678-mnop-1234",
            "first_name": "Bob",
            "last_name": "Builder"
        }
    ]
    ```

    Notes:
    - If no users match, returns an empty list.
    - Returns 422 if query param is missing or too short.
    """
    # Build the SQL query using ILIKE for case-insensitive search
    stmt = select(User).where(
        (User.first_name.ilike(f"%{query}%")) | (User.last_name.ilike(f"%{query}%"))
    )
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users


@router.post(
    "/register",
    response_model=UserRegisterOut,
    status_code=201,
    summary="Register a new user",
    description=(
        "Registers a new user based on data received from the frontend after Cognito login. "
        "If the user already exists, returns 204 No Content."
    ),
    responses={
        201: {"description": "User created successfully"},
        204: {"description": "User already exists"},
        400: {"description": "Missing or invalid data"}
    }
)
async def register_user(
    payload: UserRegisterIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user if they are not already registered.

    Checks whether a user with the given `sub` exists. If so, returns 204 No Content.
    If not, creates a new user record in the database.

    Args:
        payload (UserRegisterIn): User data (sub, email, first name, last name).
        db (AsyncSession): SQLAlchemy async database session (injected).

    Returns:
        UserRegisterOut: A message confirming successful creation.

    Raises:
        HTTPException:
            - 400 if input data is invalid.
            - (implicitly) 500 if database commit fails.

    Example request:
    ```json
    {
        "sub": "abcd-1234-efgh-5678",
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Wonder"
    }
    ```

    Example response (201):
    ```json
    {
        "message": "User created successfully"
    }
    ```

    Notes:
    - If the user already exists, the response is 204 No Content (no body).
    """
    # Check if the user already exists in the database
    result = await db.execute(select(User).where(User.sub == payload.sub))
    user = result.scalar_one_or_none()

    if user:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Create and persist the new user
    new_user = User(
        sub=payload.sub,
        email=str(payload.email),
        first_name=payload.first_name,
        last_name=payload.last_name
    )
    db.add(new_user)
    await db.commit()

    return UserRegisterOut(message="User created successfully")
