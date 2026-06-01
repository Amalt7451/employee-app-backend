"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from database import Base
from models.entity import Entity
if TYPE_CHECKING:
    from models.employee import Employee


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Address(Entity):
    __tablename__ = "address"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    zipcode:Mapped[str]= mapped_column(String(255), nullable=True)
    employee: Mapped["Employee"]= relationship(
        "Employee",
        back_populates="addresses",)


    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "employee_id":self.employee_id,
            "city": self.city,
            "country": self.country,
            "zipcode":self.zipcode
        }