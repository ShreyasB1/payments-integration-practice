class PaymentsError(Exception):
    """Base class for every error this package raises."""


class NotFound(PaymentsError):
    def __init__(self, kind, obj_id):
        super().__init__(f"No such {kind}: {obj_id}")
        self.kind = kind
        self.obj_id = obj_id


class InvalidRequest(PaymentsError):
    """The caller sent something invalid, such as a bad amount."""


class InvalidState(PaymentsError):
    """The object isn't in a state that allows this action."""
