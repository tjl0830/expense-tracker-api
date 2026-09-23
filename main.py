from fastapi import FastAPI
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict

class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1)
    amount: float = Field(gt=0)

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float

app = FastAPI()
expenses_list = [
    {"id": 1, "description": "Lunch", "amount": 150},
    {"id": 7, "description": "Dinner", "amount": 200},
    {"id": 3, "description": "Taxi", "amount": 100}
]

@app.get("/")
def read_root():
    return {
        "message": "Hello, world!"
    }

@app.get('/expenses', response_model=list[ExpenseResponse])
def get_expenses(limit: int | None = None):

    if limit is not None:
        return expenses_list[:limit]
    else:
        return expenses_list

@app.get('/expenses/{expense_id}', response_model=ExpenseResponse)
def get_expense(expense_id: int):
    for expense in expenses_list:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")
    
@app.post('/expenses', status_code=status.HTTP_201_CREATED, response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate):
    if expenses_list:
        new_id = max(expenses["id"] for expenses in expenses_list) + 1
    else:
        new_id = 1

    new_expense = {"id": new_id, "description": expense.description, "amount": expense.amount}
    expenses_list.append(new_expense)
    return new_expense

@app.delete("/expenses/{expense_id}", response_model=ExpenseResponse)
def delete_expense(expense_id: int):
    for expense in expenses_list:
        if expense["id"] == expense_id:
            deleted_expense = expense
            expenses_list.remove(expense)
            return deleted_expense
    raise HTTPException(status_code=404, detail="Expense not found")

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseCreate):
    for item in expenses_list:
            if item["id"] == expense_id:
                item["description"] = expense.description
                item["amount"] = expense.amount                
                return item
    raise HTTPException(status_code=404, detail="Expense not found")