from database.connection import Base

from sqlalchemy import Column, ForeignKey, Table


employee_department = Table(
    "employee_department",
    Base.metadata,

    Column("employee_id",ForeignKey("employees.id"),primary_key=True),

    Column("department_id",ForeignKey("departments.id"),primary_key=True))
