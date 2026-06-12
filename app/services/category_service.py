from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository


class CategoryService:

    @staticmethod
    def create_category(db: Session, name: str, user_id: int):
        return CategoryRepository.create(db, name, user_id)

    @staticmethod
    def get_categories(db: Session, user_id: int):
        return CategoryRepository.get_all(db, user_id)

    @staticmethod
    def get_category_by_id(db: Session, category_id: int):
        return CategoryRepository.get_by_id(db, category_id)