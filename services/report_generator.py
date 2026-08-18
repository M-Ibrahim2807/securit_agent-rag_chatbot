from pathlib import Path

from app.config import settings


def generate_report(llm_review: str,) -> Path:
   
    report_path = settings.REPORT_DIR / "report.md"

    with open(report_path,"w",encoding="utf-8") as file:

        file.write("# AI Code Review Report\n\n")

        file.write(llm_review)

    return report_path