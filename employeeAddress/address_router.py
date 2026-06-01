from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from employeeAddress.address_schemas import (
    addAddress,
    AddressResponse,
    updateAddress,
    updateAddressResponse,
)
from employeeAddress.address_service import (
    add_address_service,
    delete_address_service,
    get_all_address_service,
    update_address_service,
)


router = APIRouter(prefix="/addresses", tags=["Address"])


@router.post("/{id}", status_code=status.HTTP_200_OK, response_model=AddressResponse)
async def add_address(id: int, body: addAddress, db: AsyncSession = Depends(get_db)):
    address = await add_address_service(id, body.country, body.city, body.zipcode, db)
    return address


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=list[AddressResponse]
)
async def get_all_address(id: int, db: AsyncSession = Depends(get_db)):
    all_address = await get_all_address_service(id, db)
    return all_address


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_address(id: int, db: AsyncSession = Depends(get_db)):
    await delete_address_service(id, db)
    return {"message": "address deleted"}


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=updateAddressResponse
)
async def update_address(
    id: int, body: updateAddress, db: AsyncSession = Depends(get_db)
):
    update_address = await update_address_service(
        id, body.country, body.city, body.zipcode, db
    )
    return update_address
