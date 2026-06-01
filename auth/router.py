import logging
from fastapi import APIRouter, Depends
from auth import services as auth_service
from auth.schemas import TokenResponse
from database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token = await auth_service.login(db, form.username, form.password)
    logger.info(f"User {form.username} logged in successfully")
    return TokenResponse(access_token=token)
