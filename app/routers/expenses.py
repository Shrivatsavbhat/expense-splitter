
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import Expense
from app.core import get_current_user

router = APIRouter()

@router.post("/expenses")
def create_expense(expense: Expense, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
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

@router.get("/expenses" )
def read_expenses(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    expenses= db.query(models.Expense).all()
    return expenses

@router.get("/expenses/{id}")
def read_expense(id: int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/expenses/{id}")
def delete_expense(id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return Response(status_code=204)
    
