import enum

class DamageState(enum.Enum):
    STARTED = "STARTED"
    PROCESSING = "PROCESSING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"

def StateToString(state) -> str:
    if state == DamageState.STARTED:
        return 'STARTED'
    if state == DamageState.PROCESSING:
        return 'PROCESSING'
    elif state == DamageState.APPROVED:
        return 'APPROVED'
    elif state == DamageState.REJECTED:
        return 'REJECTED'
    elif state == DamageState.CLOSED:
        return 'CLOSED'

def StringToState(string) -> str:
    if string == 'STARTED':
        return DamageState.STARTED
    if string == 'PROCESSING':
        return DamageState.PROCESSING
    elif string == 'APPROVED':
        return DamageState.APPROVED
    elif string == 'REJECTED':
        return DamageState.REJECTED
    elif string == 'CLOSED':
        return DamageState.CLOSED