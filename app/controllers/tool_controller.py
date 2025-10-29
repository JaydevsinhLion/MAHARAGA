from fastapi import Request
from pydantic import BaseModel
import math
from app.utils.logger import logger

# -------------------------------------------------------------
# schema for incoming requests
# -------------------------------------------------------------
class ToolRequest(BaseModel):
    query: str
    language: str | None = None


# =============================================================
# 1️⃣ math expression solver
# =============================================================
def solve_math_expression(expression: str) -> str:
    """evaluates basic mathematical expressions safely"""
    try:
        allowed_funcs = {
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, {"__builtins__": {}}, allowed_funcs)
        return str(result)
    except ZeroDivisionError:
        return "division by zero is not allowed."
    except Exception as e:
        logger.error(f"❌ math solver failed: {e}")
        return "invalid or unsupported mathematical expression."


# =============================================================
# 2️⃣ code explanation handler
# =============================================================
def explain_code(language: str, code: str) -> str:
    """provides a simple, human-readable explanation for a code snippet"""
    language = (language or "").lower()
    code = code.strip()

    if not code:
        return "empty code snippet provided."

    try:
        if language == "python":
            if "def" in code or "lambda" in code:
                return "this python snippet defines a function or performs an operation."
            elif "for" in code or "while" in code:
                return "this python code runs a loop or iterative logic."
            elif "if" in code:
                return "this python snippet evaluates a condition and executes logic accordingly."
            else:
                return "this is a general python statement or expression."

        elif language == "javascript":
            if "function" in code or "=>" in code:
                return "this javascript snippet defines a function."
            elif "document" in code:
                return "this snippet likely manipulates html elements using dom."
            elif "console.log" in code:
                return "this line prints output to the javascript console."
            else:
                return "this is a general javascript code fragment."

        elif language == "html":
            if "<div" in code:
                return "this html snippet defines a container or layout section."
            elif "<a" in code:
                return "this defines a hyperlink element."
            elif "<img" in code:
                return "this snippet loads or displays an image on a webpage."
            else:
                return "this is a generic html markup structure."

        elif language == "css":
            if "color" in code or "background" in code:
                return "this css code styles colors or background properties."
            elif "flex" in code or "grid" in code:
                return "this css snippet defines layout properties."
            else:
                return "this is a general css styling rule."

        else:
            return f"code explanation for '{language}' not yet supported."

    except Exception as e:
        logger.error(f"❌ code explanation failed: {e}")
        return "unable to interpret the provided code snippet."


# =============================================================
# 3️⃣ api endpoint for math solving
# =============================================================
async def solve_math(request: Request, body: ToolRequest):
    """api endpoint: solves math expression"""
    try:
        expression = body.query.strip().lower()
        if not expression:
            return {"status": "error", "message": "empty expression cannot be solved."}

        result = solve_math_expression(expression)
        return {
            "status": "success",
            "expression": expression,
            "result": result,
        }

    except Exception as e:
        logger.error(f"❌ solve_math endpoint failed: {e}")
        return {"status": "error", "message": "failed to solve the given expression."}


# =============================================================
# 4️⃣ api endpoint for code explanation
# =============================================================
async def explain_code_snippet(request: Request, body: ToolRequest):
    """api endpoint: explains code snippet logic"""
    try:
        code = body.query.strip()
        language = body.language or "unknown"

        if not code:
            return {"status": "error", "message": "empty code snippet cannot be explained."}

        explanation = explain_code(language, code)

        return {
            "status": "success",
            "language": language.lower(),
            "explanation": explanation,
        }

    except Exception as e:
        logger.error(f"❌ explain_code_snippet failed: {e}")
        return {"status": "error", "message": "failed to analyze or explain the given code."}
