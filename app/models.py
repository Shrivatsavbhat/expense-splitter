from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key = True, index=True)
    description = Column(String, nullable=False)
    amount= Column(Float, nullable=False)
    paid_by = Column(String,  nullable=False)
    split_between = Column(ARRAY(String), nullable=False)

