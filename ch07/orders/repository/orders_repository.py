from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from uuid import UUID

from orders.orders_service import Order
from orders.repository.models import OrderItemModel, OrderModel


class OrdersRepository:
    def __init__(self, session: Any) -> None:
        """session: a DB session / ORM session (e.g. SQLAlchemy Session)."""
        self.session = session

    def add(self, items: Sequence[Mapping[str, Any]]) -> Order:
        """Create a new OrderModel from a sequence of item mappings.

        items: iterable of dict-like objects with keys matching OrderItemModel
        """
        record: OrderModel = OrderModel(
            items=[OrderItemModel(**item) for item in items])
        self.session.add(record)
        return Order(**record.dict(), order_=record)

    def _get(self, id_: Union[str, UUID]) -> Optional[OrderModel]:
        return self.session.query(OrderModel).filter(OrderModel.id == str(id_)).first()

    def get(self, id_: Union[str, UUID]) -> Optional[Order]:
        order = self._get(id_)
        if order is not None:
            return Order(**order.dict())
        return None

    def list(self, limit: Optional[int] = None, **filters: Any) -> List[Order]:
        query = self.session.query(OrderModel)
        if 'cancelled' in filters:
            cancelled = filters.pop('cancelled')
            if cancelled:
                query = query.filter(OrderModel.status == 'cancelled')
            else:
                query = query.filter(OrderModel.status != 'cancelled')
        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]

    def update(self, id_: Union[str, UUID], **payload: Any) -> Order:
        record = self._get(id_)
        if record is None:
            raise ValueError(f"Order with id {id_} not found")
        if 'items' in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [OrderItemModel(**item)
                            for item in payload.pop('items')]
        for key, value in payload.items():
            setattr(record, key, value)
        return Order(**record.dict())

    def delete(self, id_: Union[str, UUID]) -> None:
        rec = self._get(id_)
        if rec is not None:
            self.session.delete(rec)
