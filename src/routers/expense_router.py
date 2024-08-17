from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from services.expense_service import ExpenseService
from src.models.expense_model import Expense, State

router = APIRouter()

@router.post("/expenses/", response_model=Expense)
async def create_expense(expense: Expense, service: ExpenseService = Depends()):
    return service.create_expense(expense)

@router.get("/expenses/{expense_id}", response_model=Expense)
async def get_expense(expense_id: UUID, service: ExpenseService = Depends()):
    expense = service.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/expenses/{expense_id}", response_model=Expense)
async def update_expense(expense_id: UUID, updated_data: dict, service: ExpenseService = Depends()):
    updated_expense = service.update_expense(expense_id, updated_data)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense

@router.delete("/expenses/{expense_id}", response_model=bool)
async def delete_expense(expense_id: UUID, service: ExpenseService = Depends()):
    if not service.delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return True

@router.get("/expenses/", response_model=List[Expense])
async def get_expenses_by_state(state: State, service: ExpenseService = Depends()):
    return service.get_expenses_by_state(state)
