from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import require_role
from database import get_db

from employee_department.emp_dept_service import (
    assign_department_service,
    get_departments_of_employee_service,
    get_employees_of_department_service,
    remove_department_service,
)

from models.employee import EmployeeRole
from employee_department.emp_dept_schemas import (
    DepartmentResponse,
    EmployeeInDepartmentResponse,
)

router = APIRouter(
    prefix="/emp-dept",
    tags=["Employee Department"],
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)


@router.post(
    "/{employee_id}/{department_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[],
)
async def assign_department(
    employee_id: int, department_id: int, db: AsyncSession = Depends(get_db)
):
    await assign_department_service(employee_id, department_id, db)
    return {"message": "department assigned"}


@router.get("/{employee_id}", response_model=list[DepartmentResponse])
async def get_departments_of_employee(
    employee_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_departments_of_employee_service(employee_id, db)


@router.delete("/{employee_id}/{department_id}")
async def remove_department(
    employee_id: int, department_id: int, db: AsyncSession = Depends(get_db)
):
    await remove_department_service(employee_id, department_id, db)
    return {"message": "department deleted"}


@router.get(
    "/department/{department_id}", response_model=list[EmployeeInDepartmentResponse]
)
async def get_employees_of_department(
    department_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_employees_of_department_service(department_id, db)
