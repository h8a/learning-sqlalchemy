import asyncio
from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, String, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncConnection
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from connection import async_engine, db_psql_session


class BaseModel(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    pass


class CommonMixin(MappedAsDataclass):
    __abstract__ = True

    class Status(str, Enum):
        ENABLE = "1"
        DISABLE = "0"

    @declared_attr
    def status(cls) -> Mapped[str]:
        return mapped_column(String(2), default=cls.Status.ENABLE.value, nullable=False)

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True), default_factory=datetime.now, nullable=False
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            onupdate=datetime.now,
            nullable=False,
            default_factory=datetime.now,
        )


def generate_uuid4() -> str:
    return str(uuid4())


class ItemModel(BaseModel, CommonMixin, MappedAsDataclass):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    id_item: Mapped[str] = mapped_column(
        String(50), init=False, default_factory=generate_uuid4, primary_key=True
    )

    def __repr__(self) -> str:
        return (
            f"ItemModel(id_item={self.id_item!r}, name={self.name!r}, "
            f"status={self.status!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})"
        )


async def create_tables(connection: AsyncConnection):
    try:
        await connection.run_sync(BaseModel.metadata.create_all)
        print("Databases created")
    except Exception as e:
        print(f"Error trying create tables: {e}")


async def main():
    async with async_engine.begin() as conn:
        await create_tables(connection=conn)

    session = await db_psql_session()
    await session.begin()
    result = await session.execute(select(ItemModel))
    print("RESULT: ", result.all())


if __name__ == "__main__":
    asyncio.run(main())
