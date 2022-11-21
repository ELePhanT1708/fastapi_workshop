from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from workshop import tables
from workshop.database import get_session
from workshop.models.operations import OperationKind, OperationCreate, OperationUpdate


class OperationsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, operation_id: int) -> tables.Operation:
        operation = self.session.query(tables.Operation).filter_by(id=operation_id).first()
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, kind: Optional[OperationKind] = None) -> List[tables.Operation]:
        query = self.session.query(tables.Operation)
        if kind:
            query = query.filter_by(operation=kind)
        operations = query.all()
        return operations

    def create(self, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(**operation_data.dict())
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        operation = self._get(operation_id)
        for key, value in operation_data:
            setattr(operation, key, value)
        self.session.commit()
        return operation

    def delete(self, operation_id: int) -> None:
        operation = self._get(operation_id)
        self.session.delete(operation)
        self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
