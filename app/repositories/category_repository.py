from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:

    @staticmethod
    def create(db: Session, name: str, user_id: int) -> Category:
        category = Category(name=name, user_id=user_id)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_all(db: Session, user_id: int) -> list[Category]:
        return db.query(Category).filter(Category.user_id == user_id).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Category | None:
        return db.query(Category).filter(Category.id == category_id).first()