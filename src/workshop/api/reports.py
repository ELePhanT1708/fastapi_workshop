
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from workshop import tables
from workshop.services.auth import get_current_user
from workshop.services.reports import ReportService
from workshop.tables import Operation, User

router = APIRouter(
    prefix='/reports',
    tags=['reports']
)


@router.post('/import', name='Import CSV file')
def import_csv(
        user: User = Depends(get_current_user),
        report_service: ReportService = Depends(),
        file: UploadFile = File(...)
):
    report_service.import_csv(user.id, file.file)


@router.get('/export', name='Export CSV file')
def export_csv(
        user: User = Depends(get_current_user),
        report_service: ReportService = Depends(),
) -> StreamingResponse:
    file = report_service.export_csv(user_id=user.id)
    return StreamingResponse(
        file,
        media_type='txt/csv',
        headers={
            'Content-Disposition': 'attachment; filename=report.csv'
        }
    )


