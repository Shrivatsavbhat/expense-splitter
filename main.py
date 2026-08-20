from fastapi import FastAPI, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List
from pydantic import model_validator
from sqlalchemy.orm import Session  
#Import from the files
from app.database import engine, get_db
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
def create_expense(expense: Expense, db: Session = Depends(get_db)):
    db_expense = models.Expense(
    description=expense.description,
    amount=expense.amount,
    paid_by=expense.paid_by,
    split_between=expense.split_between

    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses")
def read_expenses(db:Session = Depends(get_db)):
    expenses= db.query(models.Expense).all()
    return expenses

@app.get("/expenses/{id}")
def read_expense(id: int, db:Session = Depends(get_db)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@app.delete("/expenses/{id}")
def delete_expense(id:int, db:Session = Depends(get_db)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return Response(status_code=204)
    
@app.get("/")
def read_root():
    return {"message":" Hello World"}