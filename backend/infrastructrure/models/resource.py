import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class Resource(Base):
    __tablename__ = 'resources'
    uuid: Mapped[str] = mapped_column(
        'uuid',
        sa.Uuid,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(sa.String(1024))
    url: Mapped[str] = mapped_column(sa.String(1024))
    xpath: Mapped[str] = mapped_column(sa.String(1024))
