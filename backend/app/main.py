import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.interests_router import interest_router
from app.api.picture_router import picture_router
from app.api.recommendations_router import rec_router
from app.modules.settings.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Startup here
    yield
    # Shutdown here


# -----
# Cors
# -----
allowed_origins = [
    "https://accounts.google.com",
]
if settings.is_debug:
    allowed_origins += [
        "http://localhost:4200",
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8000"
    ]

app_name = "North Start Compass"

# -----
# Middleware
# -----
middleware = []

# -----
# App definition
# -----
app = FastAPI(lifespan=lifespan,
              title=f"{app_name} API",
              docs_url="/docs",
              terms_of_service="/tos",
              contact={"email": f"info@{app_name}.be"},
              licence_info={f"MIT License Copyright (c) 2023 {app_name}"},
              middleware=middleware
              )


app.include_router(interest_router)
app.include_router(rec_router)
app.include_router(picture_router)

# Adding cors last
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ----
# Exception interceptors
# https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers
# ----
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return validation_intercept(request=request, exception=exc)


if __name__ == "__main__":
    reload = settings.is_debug  # If running in local environment, reload the server on changes
    try:
        uvicorn.run("main:app", host="0.0.0.0", reload=reload, port=8000)
    except Exception as e:
        print(f"Initializing app failed: {e}")
