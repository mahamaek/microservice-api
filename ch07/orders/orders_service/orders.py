class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size


class Order:
    def __init__(self, id, created, items, status, schedule_id=None, delivery_id=None, order_=None):
        self._id = id
        self._order = order_
        self._created = created
        self.items = items
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id

    @property
    def id(self):
        return self._id or self.order_.id

    @property
    def created(self):
        return self._created or self.order_.created

    def status(self):
        return self._status or self.order_.status
