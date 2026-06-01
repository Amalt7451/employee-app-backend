from sqlalchemy.ext.asyncio import AsyncSession
from departments.departments_repo import create_department_repo, get_all_department_repo, get_department_by_id_repo,update_department_repo,delete_department_repo
from exceptions import BadRequestException, NotFoundException

async def create_department_service(db: AsyncSession,name: str):
    if not name.strip():
        raise BadRequestException("name cannot be empty")
    return await create_department_repo(db,name.strip())


async def get_all_department_service(db: AsyncSession):
    all_departments=await get_all_department_repo(db)
    return all_departments

async def get_department_by_id_service(department_id: int,db: AsyncSession):
    if department_id <= 0:
        raise BadRequestException("invalid department id")
    department = await get_department_by_id_repo(department_id,db)
    if department is None:
        raise NotFoundException("department not found")
    return department

async def update_department_service(id:int,name:str,db:AsyncSession):
    if id<=0:
        raise BadRequestException("invaid department id")
    department= await update_department_repo(id,name,db)
    return department

async def delete_department_service(id:int,db:AsyncSession):
    if id<=0:
        raise BadRequestException("invaid department id")
    await delete_department_repo(id,db)


