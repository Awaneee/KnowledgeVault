from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.category import (
    CategoryCreate,
    CategoryResponse
)

from app.services.category_service import (
    CategoryService
)

router = APIRouter()


@router.post(
    "/categories",
    response_model=CategoryResponse
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return CategoryService.create_category(
        db=db,
        name=category.name,
        user_id=1
    )


@router.get(
    "/categories",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return CategoryService.get_categories(db)