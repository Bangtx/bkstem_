from fastapi import APIRouter, Depends

from .endpoints import (
    auth
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# api_router.include_router(
#     home.router,
#     prefix="/home",
#     tags=["home"],
#     dependencies=[Depends(Auth())],
# )
