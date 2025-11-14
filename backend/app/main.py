from fastapi import FastAPI
from app.api.routes import proxy
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(proxy.router)
