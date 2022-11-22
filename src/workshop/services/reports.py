import csv
from io import StringIO
from typing import Any, BinaryIO

from fastapi import Depends
from collections import OrderedDict

from workshop.models.operations import OperationCreate
from workshop.services.operations import OperationsService


class ReportService:
    def __init__(self, operation_service: OperationsService = Depends()):
        self.operation_service = operation_service

    def import_csv(self, user_id: int, file: BinaryIO):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                'date',
                'operation',
                'amount',
                'description'
            ],
        )
        next(reader, None)  # Skip the header
        operations_data = []
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations_data.append(operation_data)
        self.operation_service.create_many(
            user_id,
            operations_data,
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'operation',
                'amount',
                'description'
            ],
            extrasaction='ignore'
        )
        operations = self.operation_service.get_list(user_id=user_id)
        writer.writeheader()
        for operation in operations:
            operation_data = OperationCreate.from_orm(operation)
            writer.writerow(OrderedDict(operation_data))
        output.seek(0)
        return output
