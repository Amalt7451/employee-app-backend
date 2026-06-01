


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.emp_dept import employee_department
from models.entity import Entity


class Department(Entity):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    employees = relationship(
        "Employee",
        secondary=employee_department,
        back_populates="departments"
    )