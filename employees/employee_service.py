from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
from models.employee import Employee
from employees import employee_repo
from auth.utils import hash_password
from employees.employee_repo import (
    check_email_exists_repo,
    get_employee_by_id_repo,
    update_employee_repo,
)


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
    hashed = hash_password(password)
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name must be a non-empty string",
        )
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email must be a non-empty string",
        )
    employee = await employee_repo.create_employee(
        db,
        name.strip(),
        email.strip(),
        age,
        salary,
        hashed,
        role,
        country,
        city,
        zipcode,
    )
    return employee


async def delete_employee(id: int, db: AsyncSession) -> Employee:
    return await employee_repo.delete_employee(id, db)


async def get_all_employee(db: AsyncSession) -> Employee:
    allEmployee = await employee_repo.get_all_employee(db)
    return allEmployee


async def update_employee_service(db: AsyncSession, id: int, name: str, email: str):
    if id <= 0:
        raise BadRequestException("enter valid employee id")
    if email:
        existing_employee = await check_email_exists_repo(email, db)
        if existing_employee and existing_employee.id != id:
            raise BadRequestException("email already exists")
    employee = await update_employee_repo(db, id, name, email)
    if employee is None:
        raise NotFoundException(f"employee with id{id} not found")
    return employee


async def get_employee_by_id_service(emp_id: int, db):
    if emp_id <= 0:
        raise BadRequestException("enter valid employee id")
    employee = await get_employee_by_id_repo(emp_id, db)

    if employee is None:
        raise NotFoundException(f"employee with id{emp_id} not found")
    return employee
