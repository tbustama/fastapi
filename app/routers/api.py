from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/records/", response_model=schemas.DataRecord)
def create_record(record: schemas.DataRecordCreate, db: Session = Depends(get_db)):
    return crud.create_data_record(db, record)

@router.get("/records/", response_model=List[schemas.DataRecord])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = crud.get_data_records(db, skip, limit)
    return records

@router.get("/records/{record_id}", response_model=schemas.DataRecord)
def read_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_data_record(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record