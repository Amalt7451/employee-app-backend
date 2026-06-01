from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class DepartmentResponseID(DepartmentResponse):
    created_at: datetime
    updated_at: datetime | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = None
