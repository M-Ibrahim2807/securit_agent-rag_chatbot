from pydantic import BaseModel,HttpUrl,Field

class Analayzerequest(BaseModel):
    repo_url:HttpUrl=Field(...,
                           description="Public Github repository URL"

    )

class RepositoryQuestionRequest(BaseModel):
    question:str=Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Question about the repository"
    )