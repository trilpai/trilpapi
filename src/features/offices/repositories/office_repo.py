from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.features.offices.models.offices import Office
from src.features.offices.schemas.office_schemas import OfficeCreate, OfficeUpdate
from datetime import datetime
from typing import List, Optional


class OfficeRepository:
    """
    Repository class for performing CRUD operations on Office entities.
    """

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> Optional[Office]:
        """
        Fetch an office by its unique code.

        Args:
            db (AsyncSession): The database session.
            code (str): The unique code of the office.

        Returns:
            Optional[Office]: The Office instance if found, otherwise None.
        """
        query = select(Office).where(Office.code == code)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession, skip: int = 0, limit: int = 10, active: Optional[bool] = None
    ) -> List[Office]:
        """
        Fetch all offices with optional pagination and filtering by active status.

        Args:
            db (AsyncSession): The database session.
            skip (int): The number of records to skip.
            limit (int): The maximum number of records to return.
            active (Optional[bool]): Filter by active status if specified.

        Returns:
            List[Office]: A list of Office instances.
        """
        query = select(Office).offset(skip).limit(limit)
        if active is not None:
            query = query.where(Office.active == active)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: OfficeCreate) -> Office:
        """
        Create a new office in the database.

        Args:
            db (AsyncSession): The database session.
            data (OfficeCreate): The data for the new office.

        Returns:
            Office: The newly created Office instance.
        """
        new_office = Office(**data.dict())
        db.add(new_office)
        await db.commit()
        await db.refresh(new_office)
        return new_office

    @staticmethod
    async def update(db: AsyncSession, code: str, data: OfficeUpdate) -> Optional[Office]:
        """
        Update an existing office.

        Args:
            db (AsyncSession): The database session.
            code (str): The unique code of the office to update.
            data (OfficeUpdate): The updated office data.

        Returns:
            Optional[Office]: The updated Office instance if found, otherwise None.
        """
        office = await OfficeRepository.get_by_code(db, code)
        if not office:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(office, key, value)
        await db.commit()
        await db.refresh(office)
        return office

    @staticmethod
    async def deactivate(db: AsyncSession, code: str) -> Optional[Office]:
        """
        Deactivate an office by setting its active status to False.

        Args:
            db (AsyncSession): The database session.
            code (str): The unique code of the office to deactivate.

        Returns:
            Optional[Office]: The deactivated Office instance if found, otherwise None.
        """
        office = await OfficeRepository.get_by_code(db, code)
        if not office:
            return None
        office.active = False
        await db.commit()
        await db.refresh(office)
        return office

    @staticmethod
    async def soft_delete(db: AsyncSession, code: str) -> Optional[Office]:
        """
        Soft delete an office by setting the deleted_at timestamp.

        Args:
            db (AsyncSession): The database session.
            code (str): The unique code of the office to soft delete.

        Returns:
            Optional[Office]: The soft-deleted Office instance if found, otherwise None.
        """
        office = await OfficeRepository.get_by_code(db, code)
        if not office:
            return None
        office.deleted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(office)
        return office

    @staticmethod
    async def delete_permanent(db: AsyncSession, code: str) -> bool:
        """
        Permanently delete an office from the database.

        Args:
            db (AsyncSession): The database session.
            code (str): The unique code of the office to delete.

        Returns:
            bool: True if the office was deleted, False otherwise.
        """
        office = await OfficeRepository.get_by_code(db, code)
        if not office:
            return False
        await db.delete(office)
        await db.commit()
        return True
