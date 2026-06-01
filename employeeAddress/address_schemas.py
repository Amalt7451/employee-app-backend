

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class addAddress(BaseModel):
    model_config=ConfigDict(str_strip_whitespace=True,extra="forbid")
    country:str
    city:str
    zipcode:str

class AddressResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    employee_id:int
    country:str
    city:str
    zipcode:str
class updateAddressResponse(AddressResponse):
    created_at:datetime
    updated_at:datetime | None = None


class updateAddress(BaseModel):
    
    model_config=ConfigDict(from_attributes=True)
    country:str |None = None
    city:str | None = None
    zipcode:str |None = None









