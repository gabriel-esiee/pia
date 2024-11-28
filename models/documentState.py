import enum

class DocumentState(enum.Enum):
    REQUESTED = "REQUESTED"
    UPLOADED = "UPLOADED"

def StateToString(state) -> str:
    if state == DocumentState.REQUESTED:
        return 'REQUESTED'
    elif state == DocumentState.UPLOADED:
        return 'UPLOADED'

def StringToState(string) -> str:
    if string == 'REQUESTED':
        return DocumentState.REQUESTED
    elif string == 'UPLOADED':
        return DocumentState.UPLOADED
