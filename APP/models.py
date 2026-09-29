from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base


class Interaction(Base):

    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    task: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    user_input: Mapped[str] = mapped_column(
        Text
    )

    response: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )