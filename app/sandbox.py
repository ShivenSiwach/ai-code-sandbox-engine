import subprocess
import tempfile
import os
import time

def execute_untrusted_code(code: str, timeout_seconds: int = 3) -> dict:
    """
    Creates a temporary file, mounts it to an isolated, ephemeral Docker container,
    executes the code, and instantly destroys the container.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "script.py")
        
        # Write the untrusted code to the temp file
        with open(file_path, "w") as f:
            f.write(code)
            
        # Docker security configurations:
        # --rm: Destroy container immediately after execution
        # --network none: Prevent code from making external API/web calls
        # --memory 128m: Prevent memory leak attacks
        cmd = [
            "docker", "run", "--rm", 
            "--network", "none",
            "--memory", "128m",
            "-v", f"{temp_dir}:/usr/src/app",
            "-w", "/usr/src/app",
            "python:3.11-slim",
            "python", "script.py"
        ]
        
        start_time = time.time()
        
        try:
            # Execute the Docker command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            
            execution_time = round(time.time() - start_time, 3)
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time_seconds": execution_time
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": f"Process terminated: Code execution exceeded the {timeout_seconds}s limit.",
                "execution_time_seconds": timeout_seconds
            }