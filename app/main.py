from fastapi import FastAPI
from ariadne import QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from app.database import engine
from app.models import Base
from app.routers.api import router as api_router
from app.graphql.resolvers import query, mutation

# Initialize FastAPI app
app = FastAPI(title="UpSmith FastAPI + GraphQL Boilerplate")

# Create database tables
Base.metadata.create_all(bind=engine)

# Load GraphQL schema
with open("app/graphql/schema.graphql") as file:
    type_defs = gql(file.read())

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, query, mutation)

# Mount GraphQL endpoint
graphql_app = GraphQL(schema, debug=True)
app.mount("/graphql", graphql_app)

# Include REST API routes
app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI + GraphQL Boilerplate is running"}