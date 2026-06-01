from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, verify_password
from employees import employee_repo
from exceptions import UnauthorizedException



async def login(db:AsyncSession, email:str,password:str)->str:
    employee=await employee_repo.get_by_email(db,email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    token=  create_access_token({"id":employee.id,"email":employee.email,"role":employee.role.value})
    return token