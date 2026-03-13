import strawberry
from strawberry.types import Info
from services.user_service import get_user_by_email, create_user
from services.auth_service import create_access_token, create_refresh_token

@strawberry.type
class AuthPayload:
    access_token: str
    refresh_token: str
    user_id: str
    email: str

@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def register(self, email: str, password: str, info: Info) -> AuthPayload:
        db = info.context["db"]

        existing_user = await get_user_by_email(db, email)
        if existing_user:
            raise Exception("Email already registered")

        user = await create_user(db, email, password)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return AuthPayload(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email
        )