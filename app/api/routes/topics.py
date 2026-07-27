from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User

from app.services.topic_services import TopicService


router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)


@router.get("/")
def get_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    service = TopicService(db)

    return service.generate_topics(
        user_id=current_user.id
    )