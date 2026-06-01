"""Employee repo"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.employee import Employee
from datetime import datetime
from sqlalchemy import select
from models.Address import Address


async def get_by_email(db: AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )
    result = await db.scalars(stmt)
    return result.first()


async def create_employee(
    db: AsyncSession,
    name: str,
    email: str,
    age: int,
    salary: int,
    password: str,
    role: str,
    country: str,
    city: str,
    zipcode: str,
) -> Employee:
    db_employee = Employee(
        name=name,
        email=email,
        age=age,
        salary=salary,
        password_hash=password,
        role=role,
    )
    db_employee.addresses.append(Address(country=country, city=city, zipcode=zipcode))
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email.strip()}' is already in use",
        )
    await db.refresh(db_employee)
    return db_employee


async def delete_employee(id: int, db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.id == id, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    result.deleted_at = datetime.now()
    await db.commit()
    return


async def get_all_employee(db: AsyncSession) -> Employee:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    allEmployee = await db.scalars(stmt)
    return allEmployee


async def update_employee_repo(db: AsyncSession, id: int, name: str, email: str):
    stmt = select(Employee).where(Employee.id == id, Employee.deleted_at.is_(None))
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    if employee is None:
        return None
    if name:
        employee.name = name

    if email:
        employee.email = email

    await db.commit()
    await db.refresh(employee)
    return employee


async def check_email_exists_repo(email: str, db: AsyncSession):
    stmt = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )
    result = await db.execute(stmt)
    employee_email = result.scalar_one_or_none()
    return employee_email


async def get_employee_by_id_repo(emp_id: int, db: AsyncSession):
    stmt = select(Employee).where(Employee.id == emp_id, Employee.deleted_at.is_(None))
    result = await db.execute(stmt)
    employee = result.scalar_one_or_none()
    return employee
