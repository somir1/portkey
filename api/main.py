from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from database import init_db
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Portkey is running"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}