import enum

class DamageState(enum.Enum):
    STARTED = "STARTED"
    PROCESSING = "PROCESSING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"
