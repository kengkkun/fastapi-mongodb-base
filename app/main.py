import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.database import instance


app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.API_V1_STR)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    from app import models

    for name in dir(models):
        obj = getattr(models, name)
        try:
            if isinstance(obj, type):
                await obj.ensure_indexes()
        except:
            pass


@app.get("/health-check", status_code=200)
async def health_check() -> str:
    """
    Health Check.
    """
    return "OK"


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
