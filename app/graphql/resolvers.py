from ariadne import QueryType, MutationType
from app import crud, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

query = QueryType()
mutation = MutationType()

@query.field("getDataRecord")
def resolve_get_data_record(_, info, id):
    db: Session = next(get_db())
    record = crud.get_data_record(db, id)
    return record

@query.field("getDataRecords")
def resolve_get_data_records(_, info, skip=0, limit=100):
    db: Session = next(get_db())
    records = crud.get_data_records(db, skip, limit)
    return records

@mutation.field("createDataRecord")
def resolve_create_data_record(_, info, name, value, category=None):
    db: Session = next(get_db())
    record_input = schemas.DataRecordCreate(name=name, value=value, category=category)
    record = crud.create_data_record(db, record_input)
    return record