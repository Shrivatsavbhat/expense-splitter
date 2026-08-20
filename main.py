from fastapi import FastAPI

  
#Import from the files
from app.routers import expenses
from app.database import engine
from app import models

app= FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(expenses.router)

@app.get("/")
def read_root():
    return {"message":" Welcome to Expense-Splitter"}
