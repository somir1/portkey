from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from database import init_db, get_db
from resolvers.auth import AuthMutation
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Portkey is running"

async def get_context(db=Depends(get_db)):
    return {"db": db}

schema = strawberry.Schema(query=Query, mutation=AuthMutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}