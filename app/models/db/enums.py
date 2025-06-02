from enum import Enum

class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Language(Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    C = "C"
    CPP = "CPP"

class SubmissionState(Enum):    
    RECEIVED = "Received"
    PROCESSING = "Processing"
    COMPLETED = "Completed"