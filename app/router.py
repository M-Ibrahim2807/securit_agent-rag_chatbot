from fastapi import APIRouter, HTTPException

from models.request_models import (
    Analayzerequest,
    RepositoryQuestionRequest,
)

from services.clone_repo import clone_repository
from services.proj_val import validate_project
from services.file_reader import read_python_files
from services.bandit_runner import run_bandit
from services.semgrep_runner import run_semgrep
from services.llm import review_repository
from services.report_generator import generate_report
from rag.indexer import index_repository
from services.repository_assistant import answer_repository_question

router=APIRouter(prefix="",tags=['AI_code_review'])

@router.post("/analyze")
async def analyze_repository(request:Analayzerequest):
    try:
        repository_path=clone_repository(str(request.repo_url))

        validate_project(repository_path)

        python_files=read_python_files(repository_path)

        bandit_result=run_bandit(repository_path)
        semgrep_result=run_semgrep(repository_path)

        llm_review=review_repository(python_files,bandit_result,semgrep_result)

        report_path = generate_report(llm_review)
        indexed_chunks = index_repository(repository_path)

        return {
            "status": "success",
            "message": "Repository reviewed successfully.",
            "report_path": str(report_path),
            "indexed_chunks": indexed_chunks,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/ask")
async def ask_repository(request: RepositoryQuestionRequest):
    try:
        return answer_repository_question(request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
