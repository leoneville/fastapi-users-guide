from typing import Optional
import uuid

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    registry,
    relationship
)

table_registry = registry()

@table_registry.mapped_as_dataclass
class OAuthAccount(
    SQLAlchemyBaseOAuthAccountTableUUID
):
    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default_factory=uuid.uuid4
    )
    @declared_attr
    def user_id(cls) -> Mapped[GUID]:
        return mapped_column(
            GUID, 
            ForeignKey("user.id", ondelete="cascade"), 
            nullable=False, 
            default=None
        )
    oauth_name: Mapped[str] = mapped_column(
        String(length=100), index=True, nullable=False, default=None
    )
    access_token: Mapped[str] = mapped_column(
        String(length=1024), nullable=False, default=None
    )
    expires_at: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=None
    )
    refresh_token: Mapped[Optional[str]] = mapped_column(
        String(length=1024), nullable=True, default=None
    )
    account_id: Mapped[str] = mapped_column(
        String(length=320), index=True, nullable=False, default=None
    )
    account_email: Mapped[str] = mapped_column(
        String(length=320), nullable=False, default=None
    )

@table_registry.mapped_as_dataclass
class User(SQLAlchemyBaseUserTableUUID):
    id: Mapped[UUID_ID] = mapped_column(
        GUID, primary_key=True, default_factory=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(length=320), 
        unique=True, 
        index=True, 
        nullable=False, 
        default=None
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False, default=None
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
    )
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        'OAuthAccount', lazy='joined', default_factory=list
    )