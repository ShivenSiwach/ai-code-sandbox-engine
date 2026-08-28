from pydantic import BaseModel, Field

class CodePayload(BaseModel):
    code: str = Field(..., example="print('Hello from the secure sandbox!')")
    timeout_seconds: int = Field(default=3, le=10, description="Maximum execution time")

class ExecutionResponse(BaseModel):
    status: str
    stdout: str
    stderr: str
    execution_time_seconds: float