from langchain_groq import  ChatGroq
from langchain_core.messages import HumanMessage
from app.config import settings

llm=ChatGroq(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE,
    api_key=settings.GROQ_API_KEY

)

def review_repository(python_files:list,bandit_results:list,semgrep_results:list)->str:
    source_code=""
    print(type(python_files))
      
    print(type(python_files[0]))
    print(python_files[0])
    for file in python_files:
        source_code+=f" \n\n ### File:{file['relative_path']}\n"
        source_code+=file["source_code"]

    prompt=f"""You are an experienced Python Security Engineer.

            Analyze the repository using:

                1. Source Code
                2. Bandit Results
                3. Semgrep Results

            Source Code:{source_code}
            Bandit Findings:

            {bandit_results}

            Semgrep Findings:

            {semgrep_results}

            Generate a professional report with the following sections.

            1. Repository Summary

            2. Security Vulnerabilities

            3. Code Quality Issues

            4. Performance Suggestions

            5. Maintainability Suggestions

            6. Best Practices

            7. Overall Rating (out of 10)

            Return the answer in Markdown.
            """

    response = llm.invoke([
            HumanMessage(content=prompt)
        ]
    )

    return response.content