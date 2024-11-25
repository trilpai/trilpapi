from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime


class OfficeBase(BaseModel):
    code: str = Field(..., max_length=16, description="Unique identifier for the office")
    name: str = Field(..., max_length=48, description="Name of the office")
    o_type: Literal['HQ', 'BRANCH'] = Field(..., max_length=24, description="Type of office, must be 'HQ' or 'BRANCH'")
    ph_num1: Optional[str] = Field(None, max_length=16, description="Primary phone number")
    ph_num2: Optional[str] = Field(None, max_length=16, description="Secondary phone number")
    email1: Optional[EmailStr] = Field(None, description="Primary email address")
    email2: Optional[EmailStr] = Field(None, description="Secondary email address")
    website: Optional[str] = Field(None, max_length=48, description="Website URL")
    gst_num: Optional[str] = Field(None, max_length=24, description="GST number")
    pincode: Optional[str] = Field(None, max_length=8, description="Pincode or postal code")
    country: Optional[str] = Field(None, max_length=48, description="Country of the office")
    state: Optional[str] = Field(None, max_length=48, description="State or province")
    district: Optional[str] = Field(None, max_length=48, description="District or region")
    taluka: Optional[str] = Field(None, max_length=48, description="Sub-district or taluka")
    place: Optional[str] = Field(None, max_length=48, description="City or locality")
    address_line1: Optional[str] = Field(None, max_length=64, description="First line of the address")
    address_line2: Optional[str] = Field(None, max_length=64, description="Second line of the address")
    address_line3: Optional[str] = Field(None, max_length=64, description="Third line of the address")
    o_lat: Optional[float] = Field(None, description="Latitude coordinates")
    o_long: Optional[float] = Field(None, description="Longitude coordinates")
    notes: Optional[str] = Field(None, max_length=64, description="Additional notes about the office")

    class Config:
        orm_mode = True  # Ensures compatibility with SQLAlchemy ORM models


class OfficeCreate(OfficeBase):
    """
    Schema for creating a new office.
    """
    pass


class OfficeUpdate(BaseModel):
    """
    Schema for updating an existing office.
    All fields are optional.
    """
    name: Optional[str] = Field(None, max_length=48, description="Name of the office")
    o_type: Optional[Literal['HQ', 'BRANCH']] = Field(None, description="Type of office, must be 'HQ' or 'BRANCH'")
    ph_num1: Optional[str] = Field(None, max_length=16, description="Primary phone number")
    ph_num2: Optional[str] = Field(None, max_length=16, description="Secondary phone number")
    email1: Optional[EmailStr] = Field(None, description="Primary email address")
    email2: Optional[EmailStr] = Field(None, description="Secondary email address")
    website: Optional[str] = Field(None, max_length=48, description="Website URL")
    gst_num: Optional[str] = Field(None, max_length=24, description="GST number")
    pincode: Optional[str] = Field(None, max_length=8, description="Pincode or postal code")
    country: Optional[str] = Field(None, max_length=48, description="Country of the office")
    state: Optional[str] = Field(None, max_length=48, description="State or province")
    district: Optional[str] = Field(None, max_length=48, description="District or region")
    taluka: Optional[str] = Field(None, max_length=48, description="Sub-district or taluka")
    place: Optional[str] = Field(None, max_length=48, description="City or locality")
    address_line1: Optional[str] = Field(None, max_length=64, description="First line of the address")
    address_line2: Optional[str] = Field(None, max_length=64, description="Second line of the address")
    address_line3: Optional[str] = Field(None, max_length=64, description="Third line of the address")
    o_lat: Optional[float] = Field(None, description="Latitude coordinates")
    o_long: Optional[float] = Field(None, description="Longitude coordinates")
    notes: Optional[str] = Field(None, max_length=64, description="Additional notes about the office")
    active: Optional[bool] = Field(None, description="Status of the office (active/inactive)")

    class Config:
        orm_mode = True
