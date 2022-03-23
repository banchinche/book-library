from fastapi import FastAPI
# TODO: uncomment this in future
# from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME, openapi_url=f'{settings.API_V1}/openapi.json'
)

# if settings.BACKEND_CORS_ORIGINS:
#     app.add_midleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )


app.include_router(router=v1_router, prefix=settings.API_V1)
