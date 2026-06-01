from pydantic import BaseModel, ConfigDict

class EmployeeDepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    employee_id: int
    department_id: int



class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str