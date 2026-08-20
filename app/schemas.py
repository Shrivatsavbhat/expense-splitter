from pydantic import BaseModel, Field
from pydantic import model_validator
from typing import List



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


class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str