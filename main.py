from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from pydantic import model_validator
#Import from the files
from app.database import engine
from app import models

app= FastAPI()

models.Base.metadata.create_all(bind=engine)

class Expense(BaseModel):
    description: str
    amount: float = Field(..., gt=0)
    paid_by: str
    split_between: List[str]

    @model_validator(mode="after")
    def check_paid_by_in_split(self):
        if self.paid_by not in self.split_between:
            raise ValueError("Paid by must be in split between")
        return self

@app.post("/expenses")
def create_expense(expense: Expense):
    return expense

@app.get("/")
def read_root():
    return {"message":" Hello World"}