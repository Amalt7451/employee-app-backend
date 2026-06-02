from sqlalchemy.ext.asyncio import AsyncSession
from employees import employee_repo
from exceptions import UnauthorizedException
from auth.utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
    decode_access_token,
)


async def login(
    db: AsyncSession,
    email: str,
    password: str,
):
    employee = await employee_repo.get_by_email(
        db,
        email,
    )

    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(
        password,
        employee.password_hash,
    ):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token(
        {
            "id": employee.id,
            "email": employee.email,
            "role": employee.role.value,
        }
    )
    refresh_token = create_refresh_token(
        {
            "id": employee.id,
            "email": employee.email,
            "role": employee.role.value,
        }
    )
    return access_token, refresh_token


async def refresh_token_service(
    refresh_token: str,
):
    payload = decode_access_token(refresh_token)

    if payload is None:
        raise UnauthorizedException("Invalid refresh token")
    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid refresh token")
    access_token = create_access_token(
        {
            "id": payload["id"],
            "email": payload["email"],
            "role": payload["role"],
        }
    )
    return access_token
