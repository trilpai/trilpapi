from fastapi import APIRouter
from src.features.auth.routes.auth_route import router as auth_router
from src.features.offices.routes.office_route import router as office_router
# Add imports for other feature-specific routers here

# Create the main router
router = APIRouter()

# Include feature-specific routers
router.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
router.include_router(office_router, prefix="/api/v1/offices", tags=["Offices"])
# Add more routers here as needed
