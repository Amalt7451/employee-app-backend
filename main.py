from fastapi import FastAPI, Body,Depends,HTTPException, Request,status
from dataclasses import dataclass
from typing import TypedDict
import logging

from fastapi.responses import JSONResponse 
from employeeAddress.address_router import router as address_router
from employees.schemas import EmployeeResponseID
from exceptions import ConflictException, NotFoundException
from exceptions.handlers import register_exception_handlers
from middleware.logging import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime,timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database import  get_db
from models.employee import Employee
from employees.employee_router import router as employee_router
from middleware import configure_middleware
from config import settings
from auth.router import router as auth_router
from departments.departments_router import router as departments_router
from employee_department.emp_dept_router import router as emp_dept_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
@asynccontextmanager
async def lifespan(app:FastAPI):
    yield


app=FastAPI(
    title="employee app",
    description="simple employee app",
    version="1.0.0",
    lifespan=lifespan
)
register_exception_handlers(app)
configure_middleware(app)


app.include_router(employee_router)
app.include_router(address_router)
app.include_router(auth_router)
app.include_router(departments_router)
app.include_router(emp_dept_router)




@app.get("/health",tags=["Health"])
def health():
    return {"status":"healthy"}

    