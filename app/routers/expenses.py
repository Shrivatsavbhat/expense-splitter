from fastapi import APIRouter

router = APIRouter()

@router.post("/expenses")
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

@router.get("/expenses")
def read_expenses(db:Session = Depends(get_db)):
    expenses= db.query(models.Expense).all()
    return expenses

@router.get("/expenses/{id}")
def read_expense(id: int, db:Session = Depends(get_db)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/expenses/{id}")
def delete_expense(id:int, db:Session = Depends(get_db)):
    expense= db.query(models.Expense).filter(models.Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return Response(status_code=204)
    
@router.get("/")
def read_root():
    return {"message":" Hello World"}