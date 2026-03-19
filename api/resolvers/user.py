import strawberry


@strawberry.type
class UserType:
    id: str
    email: str
    first_name: str | None
    last_name: str | None
