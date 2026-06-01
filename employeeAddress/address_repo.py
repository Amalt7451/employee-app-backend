from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from exceptions import NotFoundException
from models.Address import Address
from models.employee import Employee

async def add_address_repo(id:int,country:str,city:str,zipcode:int,db:AsyncSession):
    stmt=select(Employee).where(Employee.id==id)
    employee= await db.scalar(stmt)
    if employee is None:
        raise NotFoundException(f"employee with id {id} not found")
    address=Address(employee_id=id,country=country,city=city,zipcode=zipcode)
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


async def get_all_address_repo(id:int,db:AsyncSession):
    stmt=select(Address).where(Address.employee_id==id,Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def delete_address_repo(address_id:int,db:AsyncSession):
    stmt=select(Address).where(Address.id==address_id,Address.deleted_at.is_(None))
    address = await db.scalar(stmt)
    if address is None:
        raise NotFoundException("address not found")
    address.deleted_at=datetime.now()
    await db.commit()


async def update_address_repo(address_id:int,country:str,city:str,zipcode:str,db:AsyncSession):
    stmt=select(Address).where(Address.id==address_id,Address.deleted_at.is_(None))
    address = await db.scalar(stmt)
    if address is None:
        raise NotFoundException("address not found")
    if country:
        address.country=country
    if city:
        address.city=city
    if zipcode:
        address.zipcode=zipcode
    await db.commit()
    await db.refresh(address)
    return address
