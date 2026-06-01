from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from employees import employee_service
from employees.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeResponseID,
    EmployeeResponseUpdate,
    EmployeeUpdate,
)
from auth.dependencies import get_current_user, require_role
from auth.schemas import TokenPayload
from employees.employee_service import (
    get_employee_by_id_service,
    update_employee_service,
)
from models.employee import EmployeeRole

router = APIRouter(prefix="/employee", tags=["Employee"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(body: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.create_employee(
        db,
        body.name,
        body.email,
        body.age,
        body.salary,
        body.password,
        body.role,
        body.address.country,
        body.address.city,
        body.address.zipcode,
    )
    return employee


@router.delete(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    await employee_service.delete_employee(id, db)
    return {"message": "employee deleted"}


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    allEmployee = await employee_service.get_all_employee(db)
    return allEmployee


@router.patch(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponseUpdate,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update_employee(
    id: int, body: EmployeeUpdate, db: AsyncSession = Depends(get_db)
):
    employee = await update_employee_service(db, id, body.name, body.email)
    return employee


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponseID,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def get_employee_by_id(id: int, db: AsyncSession = Depends(get_db)):
    employee = await get_employee_by_id_service(id, db)
    return employee
