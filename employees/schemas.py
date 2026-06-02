from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from models.employee import EmployeeRole


class AddressCreate(BaseModel):
    country: str
    city: str
    zipcode: str


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
