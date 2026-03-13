from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from services.auth_service import hash_password
import uuid


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
):
    hashed = hash_password(password)
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password=hashed,
        first_name=first_name,
        last_name=last_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_refresh_token(db: AsyncSession, user: User, refresh_token: str):
    user.refresh_token = refresh_token
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def clear_refresh_token(db: AsyncSession, user: User):
    user.refresh_token = None
    await db.commit()
    await db.refresh(user)
    return user