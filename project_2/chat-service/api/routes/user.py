# api/routes/user.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.db.deps import get_db
from api.models.user import User
from api.schemas.user import UserSearchOut

router = APIRouter()

@router.get(
    "/users/search",
    response_model=list[UserSearchOut],
    summary="Search users by name",
    description="Returns users whose first name or last name contains the given query string (case-insensitive)."
)
async def search_users(query: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(
        (User.first_name.ilike(f"%{query}%")) | (User.last_name.ilike(f"%{query}%"))
    )
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users
