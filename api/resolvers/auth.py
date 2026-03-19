import strawberry
from strawberry.types import Info

from services.user_service import (
    get_user_by_email,
    create_user,
    update_refresh_token,
    get_user_by_id,
    clear_refresh_token,
)
from services.auth_service import (
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_token,
)
from utils.validators import validate_email, validate_password, validate_name


@strawberry.type
class AuthPayload:
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    first_name: str
    last_name: str


@strawberry.type
class LogoutPayload:
    success: bool
    message: str


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        info: Info,
    ) -> AuthPayload:
        db = info.context["db"]

        email = validate_email(email)
        validate_password(password)
        first_name = validate_name(first_name, "First name")
        last_name = validate_name(last_name, "Last name")

        existing_user = await get_user_by_email(db, email)
        if existing_user:
            raise Exception("Email already registered")

        user = await create_user(db, email, password, first_name, last_name)

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        await update_refresh_token(db, user, refresh_token)

        return AuthPayload(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @strawberry.mutation
    async def login(self, email: str, password: str, info: Info) -> AuthPayload:
        db = info.context["db"]

        email = validate_email(email)
        validate_password(password)

        user = await get_user_by_email(db, email)
        if not user:
            raise Exception("Invalid email or password")

        if not verify_password(password, user.password):
            raise Exception("Invalid email or password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        await update_refresh_token(db, user, refresh_token)

        return AuthPayload(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @strawberry.mutation
    async def logout(self, info: Info) -> LogoutPayload:
        request = info.context["request"]
        db = info.context["db"]

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Exception("Authorization header missing")

        token = auth_header.replace("Bearer ", "")
        payload = decode_token(token)

        if not payload:
            raise Exception("Invalid token")

        user_id = payload.get("sub")
        user = await get_user_by_id(db, user_id)

        if not user:
            raise Exception("User not found")

        await clear_refresh_token(db, user)

        return LogoutPayload(
            success=True,
            message="Logged out successfully",
        )

    @strawberry.mutation
    async def refresh_token(self, token: str, info: Info) -> AuthPayload:
        db = info.context["db"]

        payload = decode_token(token)
        if not payload:
            raise Exception("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise Exception("Invalid token type")

        user_id = payload.get("sub")
        user = await get_user_by_id(db, user_id)

        if not user:
            raise Exception("User not found")

        if user.refresh_token != token:
            raise Exception("Refresh token mismatch")

        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)

        await update_refresh_token(db, user, new_refresh_token)

        return AuthPayload(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
