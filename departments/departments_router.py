from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth.dependencies import get_current_user
from fastapi import APIRouter, Depends, status
from departments.departments_schema import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from departments.departments_service import (
    create_department_service,
    get_all_department_service,
    get_department_by_id_service,
    update_department_service,
    delete_department_service,
)

router = APIRouter(
    prefix="/department", tags=["Department"], dependencies=[Depends(get_current_user)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    await create_department_service(db, body.name)
    return {"message": "department created"}


@router.get("", status_code=status.HTTP_200_OK, response_model=list[DepartmentResponse])
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    all_departments = await get_all_department_service(db)
    return all_departments


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=DepartmentResponse)
async def get_department_by_id(id: int, db: AsyncSession = Depends(get_db)):
    department = await get_department_by_id_service(id, db)
    return department


@router.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=DepartmentResponse
)
async def update_department(
    body: DepartmentUpdate, id: int, db: AsyncSession = Depends(get_db)
):
    department = await update_department_service(id, body.name, db)
    return department


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_department(id: int, db: AsyncSession = Depends(get_db)):
    await delete_department_service(id, db)
    return {"message": "department deleted"}
