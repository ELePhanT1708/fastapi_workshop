from fastapi import APIRouter
from .operations import router as operations_router
from .auth import router as auth_router
from .reports import router as report_router


router = APIRouter()
router.include_router(operations_router)
router.include_router(auth_router)
router.include_router(report_router)
