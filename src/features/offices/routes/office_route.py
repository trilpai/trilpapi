from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from typing import List, Optional
from src.features.offices.services.office_service import (
    create_office,
    get_office_by_id,
    get_all_offices,
    update_office,
    deactivate_office,
    soft_delete_office,
    delete_office_permanent,
    export_offices_to_xlsx,
    download_offices_xlsx_template,
    import_offices_from_xlsx,
)
from src.features.offices.schemas.office_schemas import OfficeCreate, OfficeUpdate, OfficeBase
from src.core.db import get_db

router = APIRouter()

@router.post("", response_model=OfficeBase, status_code=201)
async def create_office_endpoint(data: OfficeCreate, db=Depends(get_db)):
    """
    Create a new office.
    """
    return await create_office(db, data)

@router.get("/id/{code}", response_model=OfficeBase)
async def read_office_by_id(code: str, db=Depends(get_db)):
    """
    Retrieve an office by its unique code.
    """
    office = await get_office_by_id(db, code)
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    return office

@router.get("", response_model=List[OfficeBase])
async def read_all_offices(
    db=Depends(get_db), skip: int = 0, limit: int = 10, active: Optional[bool] = None
):
    """
    Retrieve all offices with optional pagination and filtering.
    """
    return await get_all_offices(db, skip, limit, active)

@router.get("/wop", response_model=List[OfficeBase])
async def read_all_offices_without_pagination(db=Depends(get_db)):
    """
    Retrieve all offices without pagination.
    """
    return await get_all_offices(db)

@router.put("/id/{code}", response_model=OfficeBase)
async def update_office_endpoint(code: str, data: OfficeUpdate, db=Depends(get_db)):
    """
    Update an office by its unique code.
    """
    return await update_office(db, code, data)

@router.patch("/id/{code}/deact", response_model=dict)
async def deactivate_office_endpoint(code: str, db=Depends(get_db)):
    """
    Deactivate an office by its unique code.
    """
    return await deactivate_office(db, code)

@router.patch("/id/{code}/softdelete", response_model=dict)
async def soft_delete_office_endpoint(code: str, db=Depends(get_db)):
    """
    Soft delete an office by its unique code.
    """
    return await soft_delete_office(db, code)

@router.delete("/id/{code}", response_model=dict)
async def delete_office_permanent_endpoint(code: str, db=Depends(get_db)):
    """
    Permanently delete an office by its unique code.
    """
    return await delete_office_permanent(db, code)

@router.get("/export/xlsx", response_class=FileResponse)
async def export_to_xlsx_endpoint(db=Depends(get_db)):
    """
    Export all offices to an XLSX file.
    """
    return await export_offices_to_xlsx(db)

@router.get("/xlsxtemplate", response_class=FileResponse)
async def download_xlsx_template_endpoint():
    """
    Download an XLSX template for importing office data.
    """
    return await download_offices_xlsx_template()

@router.post("/import/xlsx", response_model=dict)
async def import_from_xlsx_endpoint(file: UploadFile = File(...), db=Depends(get_db)):
    """
    Import office data from an uploaded XLSX file.
    """
    return await import_offices_from_xlsx(file, db)
