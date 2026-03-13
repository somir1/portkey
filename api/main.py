from fastapi import FastAPI, Depends, Request
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from database import init_db, get_db
from resolvers.auth import AuthMutation
from resolvers.user import UserType
from services.auth_service import decode_token
from services.user_service import get_user_by_id
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Portkey is running"

    @strawberry.field
    async def me(self, info: Info) -> UserType:
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

        return UserType(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )


async def get_context(request: Request, db=Depends(get_db)):
    return {
        "request": request,
        "db": db,
    }


schema = strawberry.Schema(query=Query, mutation=AuthMutation)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphql_ide="graphiql",
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}