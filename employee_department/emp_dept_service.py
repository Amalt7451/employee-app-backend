from exceptions import BadRequestException

from employee_department.emp_dept_repo import (
    assign_department_repo,
    get_employee_departments_repo,
    remove_department_repo,
)


async def assign_department_service(employee_id: int, department_id: int, db):
    if employee_id <= 0:
        raise BadRequestException("invalid employee id")
    if department_id <= 0:
        raise BadRequestException("invalid department id")
    await assign_department_repo(employee_id, department_id, db)


async def get_employee_departments_service(employee_id: int, db):
    if employee_id <= 0:
        raise BadRequestException("invalid employee id")

    return await get_employee_departments_repo(employee_id, db)


async def remove_department_service(employee_id: int, department_id: int, db):
    await remove_department_repo(employee_id, department_id, db)
