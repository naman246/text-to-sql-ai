from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import re 
from app.clarification import analyze_question
from app.sql_generator import generate_sql
from app.sql_executor import execute_query
from app.sql_validator import validate_sql
from app.result_formatter import format_result

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Text-to-SQL AI",
    description="AI-powered natural language database query system",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str

def contains_dangerous_intent(question: str) -> bool:
    """Detect requests that attempt to modify or destroy database data."""

    dangerous_patterns = [
        r"\bdelete\b",
        r"\bdrop\b",
        r"\btruncate\b",
        r"\bupdate\b",
        r"\binsert\b",
        r"\balter\b",
        r"\bcreate\b",
        r"\breplace\b",
    ]

    question_lower = question.lower()

    return any(
        re.search(pattern, question_lower)
        for pattern in dangerous_patterns
    )


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question
    if contains_dangerous_intent(question):
             return {
            "status": "blocked",
            "error": "This application only supports read-only database queries."
        }

    # Step 1: Check for ambiguity
    analysis = analyze_question(question)

    if analysis["needs_clarification"]:
        return {
            "status": "clarification_needed",
            "question": analysis["clarification"]
        }

    # Step 2: Generate SQL
    sql = generate_sql(question)

    # Step 3: Validate SQL
    is_valid, message = validate_sql(sql)

    if not is_valid:
        return {
            "status": "blocked",
            "sql": sql,
            "error": message
        }

    # Step 4: Execute SQL
    result = execute_query(sql)

    if "error" in result:
        return {
            "status": "error",
            "sql": sql,
            "error": result["error"]
        }

    # Step 5: Format result
    answer = format_result(
        question,
        sql,
        result
    )

    return {
        "status": "success",
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer
    }