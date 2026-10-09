from fastapi import FastAPI
from fastapi import HTTPException, status, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1)
    amount: float = Field(gt=0)

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float


app = FastAPI()
# expenses_list = [
#     {"id": 1, "description": "Lunch", "amount": 150},
#     {"id": 7, "description": "Dinner", "amount": 200},
#     {"id": 3, "description": "Taxi", "amount": 100}
# ]
expenses_list = [
    {"id": 1, "description": "Lunch", "amount": 150},
    {"id": 7, "description": "Dinner", "amount": 200},
    {"id": 3, "description": "Taxi", "amount": 100},
    {"id": 8, "description": "Coffee", "amount": 85},
    {"id": 9, "description": "Groceries", "amount": 1250},
    {"id": 10, "description": "Bus Fare", "amount": 35},
    {"id": 11, "description": "Electricity Bill", "amount": 1850},
    {"id": 12, "description": "Internet Bill", "amount": 1299},
    {"id": 13, "description": "Snacks", "amount": 65},
    {"id": 14, "description": "Movie Ticket", "amount": 280},
    {"id": 15, "description": "Mobile Load", "amount": 100},
    {"id": 16, "description": "Laundry", "amount": 180},
    {"id": 17, "description": "Fast Food", "amount": 175},
    {"id": 18, "description": "Medicine", "amount": 320},
    {"id": 19, "description": "Water Bill", "amount": 450},
    {"id": 20, "description": "Jeepney Fare", "amount": 24},
    {"id": 21, "description": "Keyboard", "amount": 2499},
    {"id": 22, "description": "Notebook", "amount": 55},
    {"id": 23, "description": "Headphones", "amount": 1599},
    {"id": 24, "description": "Pizza", "amount": 399},
    {"id": 25, "description": "Phone Case", "amount": 199},
    {"id": 26, "description": "Water", "amount": 25},
    {"id": 27, "description": "Online Subscription", "amount": 299}
]


@app.get("/")
def read_root():

    return {
        "message": "Hello, world!"
    }


@app.get('/expenses', response_model=list[ExpenseResponse])
def get_expenses(
    limit: int | None = Query(default=None, ge=1), 
    min_amount: float | None = Query(default=None, ge=0),
    sort: Literal["amount", "-amount"] | None = Query(default=None)):

    result = expenses_list.copy()

    if min_amount is not None:
        result = [expense for expense in result if expense["amount"] >= min_amount]    
    
    if sort == 'amount':
        result.sort(key=lambda x: x['amount'])
    elif sort == '-amount':
        result.sort(key=lambda x: x['amount'], reverse=True)
    
    if limit is not None:
        result = result[:limit]

    return result


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