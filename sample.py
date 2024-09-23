from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
import uuid

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

#SQLAlchemy Model (ORM)
class Department(Base):
    __tablename__ = "departments"

    id = Column(String, primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    name = Column(String, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    students = relationship("Student", back_populates= "departments")

class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    level = Column(String, default = 1)
    is_active = Column(Boolean, default=True)

    department_id = Column(String, ForeignKey("departments.id"))
    
    departments = relationship("Department", back_populates="students")

Base.metadata.create_all(bind=engine)

#PyDantic Models

class DeparmentBase(BaseModel):
    name : str
    description : str

class DepartmentResponse(BaseModel):
    id : str
    name : str
    description : str 
    is_active: bool

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    firstname : str
    lastname : str
    level : int
    department_id : str

class StudentResponse(BaseModel):
    id : str
    firstname : str
    lastname : str
    level : int
    department_id : str
    is_active : bool

    class Config:
        from_attributes = True

#Routes
@app.post("/api/departments", response_model=list[DeparmentBase])
def create_department(format: DeparmentBase, db: SessionLocal = Depends(get_db)):
    department = Department(name = format.name,
                            description = format.description)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

@app.get("/api/department", response_model=list[DeparmentBase])
def create_department(format: DeparmentBase, db: SessionLocal = Depends(get_db)):
    department = Department(name = format.name,
                            description = format.description)
    db = db.query(Department).filter(Department.is_active == True).all() 
    return department