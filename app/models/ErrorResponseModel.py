from enum import Enum

class ErrorType(Enum):
    """Error type enum."""
    #Todo: Define nomenclature for error types
    SYSTEM_ERROR = "SYSTEM-ERROR"
    VALIDATION_ERROR = "VALIDATION-ERROR"
    COMPILATION_ERROR = "COMPILATION-ERROR"

class Errors(Enum):
    SYSTEM_ERROR = ("LLDFY-300", ErrorType.SYSTEM_ERROR)
    VALIDATION_ERROR = ("LLDFY-201", ErrorType.VALIDATION_ERROR)
    COMPILATION_ERROR = ("LLDFY-400", ErrorType.COMPILATION_ERROR)

    def __init__(self, status_code, error_type):
        self._status_code = status_code
        self._error_type = error_type

    @property
    def status_code(self):
        return self._status_code

    @property
    def error_type(self):
        return self._error_type

class ErrorResponseModel:
    """Error response model."""
    def __init__(self, message: str, errorType: ErrorType, status_code: str):
        self.message = message
        self.status_code = status_code
        self.errorType = errorType
    
    def to_dict(self):
        return {
            "message": self.message,
            "status_code": self.status_code,
            "errorType": self.errorType.value
        }
    
    @classmethod
    def populate_response_model(cls, status_code: str, message: str, errorType: ErrorType):
        return cls(
            message=message,
            errorType=errorType,
            status_code=status_code
        ).to_dict()