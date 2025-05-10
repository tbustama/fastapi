from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class DataRecord(Base):
    __tablename__ = "data_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float, nullable=False)
    category = Column(String, nullable=True)