
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from exceptions import NotFoundException
from models.departments import Department


async def create_department_repo(db: AsyncSession,name: str):
    department = Department(name=name)
    db.add(department)
    await db.commit()
    await db.refresh(department)
    return department

async def get_all_department_repo(db: AsyncSession):
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()

async def get_department_by_id_repo(department_id: int,db: AsyncSession):
    stmt = select(Department).where(Department.id == department_id,Department.deleted_at.is_(None))
    department = await db.scalar(stmt)
    return department

async def update_department_repo(department_id: int,name: str,db: AsyncSession):
    stmt = select(Department).where(Department.id == department_id,Department.deleted_at.is_(None))
    department = await db.scalar(stmt)
    if department is None:
        raise NotFoundException("department not found")
    if name:
        department.name = name
    await db.commit()
    await db.refresh(department)
    return department

async def delete_department_repo(department_id: int,db: AsyncSession):
    stmt = select(Department).where(Department.id == department_id,Department.deleted_at.is_(None))
    department = await db.scalar(stmt)
    if department is None:
        raise NotFoundException(
            "department not found")
    department.deleted_at = datetime.now()
    await db.commit()