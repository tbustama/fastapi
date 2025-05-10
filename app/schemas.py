from pydantic import BaseModel
from typing import Optional

class DataRecordBase(BaseModel):
    name: str
    value: float
    category: Optional[str] = None

class DataRecordCreate(DataRecordBase):
    pass

class DataRecord(DataRecordBase):
    id: int

    class Config:
        orm_mode = True