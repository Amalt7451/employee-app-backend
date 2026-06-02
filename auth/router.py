import logging
from fastapi import APIRouter, Depends
from auth import services as auth_service

from database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import TokenResponse, RefreshRequest


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    access_token, refresh_token = await auth_service.login(
        db,
        form.username,
        form.password,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh")
async def refresh(
    body: RefreshRequest,
):
    access_token = await auth_service.refresh_token_service(body.refresh_token)

    return {"access_token": access_token}
