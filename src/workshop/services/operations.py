from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from workshop import tables
from workshop.database import get_session
from workshop.models.operations import OperationKind, OperationCreate, OperationUpdate


class OperationsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user_id: int, operation_id: int) -> tables.Operation:
        operation = self.session.query(tables.Operation)\
            .filter_by(id=operation_id,
                       user_id=user_id)\
            .first()
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, user_id: int,  kind: Optional[OperationKind] = None) -> List[tables.Operation]:
        query = self.session.query(tables.Operation).filter_by(user_id=user_id)
        if kind:
            query = query.filter_by(operation=kind)
        operations = query.all()
        return operations

    def create_many(self, user_id: int, operation_data: List[OperationCreate]) -> List[tables.Operation]:
        operations = [tables.Operation(**operation.dict(), user_id=user_id) for operation in operation_data]
        self.session.add_all(operations)
        self.session.commit()
        return operations

    def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(**operation_data.dict(), user_id=user_id)
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, user_id: int, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        operation = self._get(user_id, operation_id)
        for key, value in operation_data:
            setattr(operation, key, value)
        self.session.commit()
        return operation

    def delete(self, user_id: int, operation_id: int) -> None:
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
