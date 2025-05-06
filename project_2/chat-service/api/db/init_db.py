# api/db/init_db.py

import asyncio
from api.db.session import engine, async_session
from api.models.base import Base
from api.models.user import User
from api.models.chat import Chat
from api.models import user, chat, message

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
