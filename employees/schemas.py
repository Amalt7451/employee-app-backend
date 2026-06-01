from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from models.employee import EmployeeRole


class AddressCreate(BaseModel):
    country: str
    city: str
    zipcode: str
    # @field_validator("zipcode")
    # @classmethod
    # def zipcode(cls, v: str) -> str:
    #     if not v.isdigit():
    #         raise ValueError("zipcode must contain only digits (0-9)")
    #     return v
    # @model_validator(mode="after")

    # def zipcode_length_for_country(self):

    #     country = self.country.strip().upper()

    #     n = len(self.zipcode)

    #     if country in ("US", "USA") and n != 5:

    #         raise ValueError("US ZIP codes must be exactly 5 digits")

    #     elif country == "IN" and n != 6:

    #         raise ValueError("Indian PIN codes must be exactly 6 digits")

    #     return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: str
    age: int | None = None
    salary: int | None = None
    password: str = Field(min_lengths=6)
    role: EmployeeRole
    address: AddressCreate | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None = None


class EmployeeResponseID(EmployeeResponse):
    created_at: datetime
    updated_at: datetime


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class EmployeeResponseUpdate(EmployeeResponse):
    updated_at: datetime
