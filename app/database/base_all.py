# app/database/base_all.py
from app.database.base import Base  # noqa — Base must be imported first

from app.models.user import User          # noqa
from app.models.category import Category  # noqa
from app.models.notes import Note         # noqa
from app.models.attachment import Attachment  # noqa