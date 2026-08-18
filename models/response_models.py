from pydantic import BaseModel
from typing import Optional

class AnalayzeResponse(BaseModel):
    status:str
    message:str

class StatusResponse(BaseModel):
    status:str
    progress:int
    currenet_step:str

class RepositoryQuestionResponse(BaseModel):
    question:str
    answer:str

class ReportResponse(BaseModel):
    report_path:str
    total_issues:int
    high_severity:int
    medium_severity:int
    low_severity:int

class ErrorResponse(BaseModel):
    status:str="error"
    message:str
    details:Optional[str]=None
    