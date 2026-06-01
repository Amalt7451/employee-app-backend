from sqlalchemy import delete, insert, select

from models.employee import Employee
from models.departments import Department
from models.emp_dept import employee_department
from exceptions import NotFoundException


async def assign_department_repo(employee_id: int, department_id: int, db):
    stmt = select(Employee).where(
        Employee.id == employee_id, Employee.deleted_at.is_(None)
    )
    employee = db.scalar(stmt)
    if employee is None:
        raise NotFoundException("employee not found")
    department = await db.scalar(
        select(Department).where(
            Department.id == department_id, Department.deleted_at.is_(None)
        )
    )
    if department is None:
        raise NotFoundException("department not found")
    await db.execute(
        insert(employee_department).values(
            employee_id=employee_id, department_id=department_id
        )
    )
    await db.commit()


async def get_employee_departments_repo(employee_id: int, db):
    employee = await db.scalar(
        select(Employee).where(
            Employee.id == employee_id, Employee.deleted_at.is_(None)
        )
    )
    if employee is None:
        raise NotFoundException("employee not found")
    stmt = (
        select(Department)
        .join(employee_department, Department.id == employee_department.c.department_id)
        .where(
            employee_department.c.employee_id == employee_id,
            Department.deleted_at.is_(None),
        )
    )
    result = await db.scalars(stmt)
    return result.all()


async def remove_department_repo(employee_id: int, department_id: int, db):
    employee = await db.scalar(select(Employee).where(Employee.id == employee_id))
    if employee is None:
        raise NotFoundException("employee not found")
    department = await db.scalar(
        select(Department).where(Department.id == department_id)
    )
    if department is None:
        raise NotFoundException("department not found")
    await db.execute(
        delete(employee_department).where(
            employee_department.c.employee_id == employee_id,
            employee_department.c.department_id == department_id,
        )
    )
    await db.commit()
