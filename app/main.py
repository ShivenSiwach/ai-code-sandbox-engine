from fastapi import FastAPI, HTTPException
from app.schemas import CodePayload, ExecutionResponse
from app.sandbox import execute_untrusted_code

app = FastAPI(
    title="AI Code Execution Sandbox",
    description="Ephemeral Docker orchestration for safely executing untrusted, LLM-generated code.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "online", "service": "ephemeral-sandbox-engine"}

@app.post("/sandbox/execute", response_model=ExecutionResponse)
def run_code(payload: CodePayload):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code payload cannot be empty.")
    
    # Send code to the isolation engine
    result = execute_untrusted_code(payload.code, payload.timeout_seconds)
    
    return ExecutionResponse(
        status=result["status"],
        stdout=result["stdout"],
        stderr=result["stderr"],
        execution_time_seconds=result["execution_time_seconds"]
    )