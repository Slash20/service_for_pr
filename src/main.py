from fastapi import FastAPI

from routers.health import router as health_router
from routers.teams import router as teams_router
from routers.users import router as users_router
from routers.pull_requests import router as pull_requests_router

app = FastAPI()

app.include_router(health_router)
app.include_router(teams_router)
app.include_router(users_router)
app.include_router(pull_requests_router)