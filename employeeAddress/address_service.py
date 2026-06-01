from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException
from employeeAddress.address_repo import (
    add_address_repo,
    delete_address_repo,
    get_all_address_repo,
    update_address_repo,
)


async def add_address_service(
    id: int, country: str, city: str, zipcode: int, db: AsyncSession
):
    if id <= 0:
        raise BadRequestException("not a valid employee")
    address = await add_address_repo(id, country, city, zipcode, db)
    return address


async def get_all_address_service(id: int, db: AsyncSession):
    if id <= 0:
        raise BadRequestException("not a valid employee")
    all_address = await get_all_address_repo(id, db)
    return all_address


async def delete_address_service(id: int, db: AsyncSession):
    if id <= 0:
        raise BadRequestException("not a valid employee")
    await delete_address_repo(id, db)


async def update_address_service(
    id: int, country: str, city: str, zipcode: str, db: AsyncSession
):
    if id <= 0:
        raise BadRequestException("not a valid employee")
    address = await update_address_repo(id, country, city, zipcode, db)
    return address
