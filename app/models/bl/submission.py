from pydantic import BaseModel
from models.bl.enums import SupportedLanguages

class SubmissionRequest(BaseModel):
    problem_id: str
    lang: SupportedLanguages
    files_metadata: dict
