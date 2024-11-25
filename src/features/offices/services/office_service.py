from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from src.features.offices.models.offices import Office
from src.features.offices.schemas.office_schemas import OfficeCreate, OfficeUpdate
from src.features.offices.repositories.office_repo import OfficeRepository
from typing import List
from fastapi.responses import FileResponse
import io

async def create_office(db: AsyncSession, data: OfficeCreate) -> dict:
    """
    Create a new office in the database.

    Args:
        db (AsyncSession): The database session.
        data (OfficeCreate): The data for the new office.

    Returns:
        dict: The newly created office as a dictionary.

    Raises:
        HTTPException: If an office with the given code already exists.
    """
    existing_office = await OfficeRepository.get_by_code(db, data.code)
    if existing_office:
        raise HTTPException(status_code=400, detail="Office with this code already exists.")
    office = await OfficeRepository.create(db, data)
    return office.to_dict()

async def get_office_by_id(db: AsyncSession, code: str) -> dict:
    """
    Retrieve an office by its unique code.

    Args:
        db (AsyncSession): The database session.
        code (str): The unique code of the office.

    Returns:
        dict: The office as a dictionary.

    Raises:
        HTTPException: If the office does not exist.
    """
    office = await OfficeRepository.get_by_code(db, code)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found.")
    return office.to_dict()

async def get_all_offices(db: AsyncSession, skip: int = 0, limit: int = 10, active: bool = None) -> List[dict]:
    """
    Retrieve all offices with optional pagination and filtering.

    Args:
        db (AsyncSession): The database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.
        active (bool, optional): Filter by active status.

    Returns:
        List[dict]: A list of office dictionaries.
    """
    offices = await OfficeRepository.get_all(db, skip, limit, active)
    return [office.to_dict() for office in offices]

async def update_office(db: AsyncSession, code: str, data: OfficeUpdate) -> dict:
    """
    Update an office's details.

    Args:
        db (AsyncSession): The database session.
        code (str): The unique code of the office.
        data (OfficeUpdate): The updated office data.

    Returns:
        dict: The updated office as a dictionary.

    Raises:
        HTTPException: If the office does not exist.
    """
    office = await OfficeRepository.update(db, code, data)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found.")
    return office.to_dict()

async def deactivate_office(db: AsyncSession, code: str) -> dict:
    """
    Deactivate an office.

    Args:
        db (AsyncSession): The database session.
        code (str): The unique code of the office.

    Returns:
        dict: The deactivated office as a dictionary.

    Raises:
        HTTPException: If the office does not exist.
    """
    office = await OfficeRepository.deactivate(db, code)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found.")
    return office.to_dict()

async def soft_delete_office(db: AsyncSession, code: str) -> dict:
    """
    Perform a soft delete on an office.

    Args:
        db (AsyncSession): The database session.
        code (str): The unique code of the office.

    Returns:
        dict: The soft-deleted office as a dictionary.

    Raises:
        HTTPException: If the office does not exist.
    """
    office = await OfficeRepository.soft_delete(db, code)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found.")
    return office.to_dict()

async def delete_office_permanent(db: AsyncSession, code: str) -> dict:
    """
    Permanently delete an office.

    Args:
        db (AsyncSession): The database session.
        code (str): The unique code of the office.

    Returns:
        dict: A success message.

    Raises:
        HTTPException: If the office does not exist.
    """
    success = await OfficeRepository.delete_permanent(db, code)
    if not success:
        raise HTTPException(status_code=404, detail="Office not found.")
    return {"detail": "Office deleted permanently."}

async def export_offices_to_xlsx(db: AsyncSession) -> FileResponse:
    """
    Export all offices to an XLSX file.

    Args:
        db (AsyncSession): The database session.

    Returns:
        FileResponse: The XLSX file containing office data.
    """
    xlsx_file = await OfficeRepository.export_to_xlsx(db)
    return FileResponse(xlsx_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

async def download_offices_xlsx_template() -> FileResponse:
    """
    Download an XLSX template for importing office data.

    Returns:
        FileResponse: The XLSX template file.
    """
    template_file = "path/to/template.xlsx"
    return FileResponse(template_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

async def import_offices_from_xlsx(file: UploadFile, db: AsyncSession) -> dict:
    """
    Import office data from an XLSX file.

    Args:
        file (UploadFile): The uploaded XLSX file.
        db (AsyncSession): The database session.

    Returns:
        dict: A success message.
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an XLSX file.")
    
    file_content = await file.read()
    result = await OfficeRepository.import_from_xlsx(io.BytesIO(file_content), db)
    return {"detail": f"{result} records imported successfully."}
