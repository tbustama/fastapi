from sqlalchemy.orm import Session
from app.models import DataRecord
from app.schemas import DataRecordCreate

def create_data_record(db: Session, record: DataRecordCreate):
    db_record = DataRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_data_record(db: Session, record_id: int):
    return db.query(DataRecord).filter(DataRecord.id == record_id).first()

def get_data_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DataRecord).offset(skip).limit(limit).all()