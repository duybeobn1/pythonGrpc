from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import subprocess
import logging
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    result: str

@app.post("/api/park/test")
async def test_endpoint(request: Request):
    try:
        data = await request.json()
        command = data.get("command")
        if not command:
            raise HTTPException(status_code=400, detail="Command not provided")

        logger.info(f"Received command: {command}")

        script_map = {
            "start": r"d:\Stage Air 2024\spring\python-server\AutoExtract+Behavior\part1.py",
            "read": r"d:\Stage Air 2024\spring\python-server\AutoExtract+Behavior\part2.py",
        }

        script = script_map.get(command)
        if not script:
            raise HTTPException(status_code=400, detail="Invalid command")

        if not os.path.exists(script):
            raise HTTPException(status_code=400, detail=f"Script not found: {script}")

        logger.info(f"Executing script: {script}")

        # Use subprocess.Popen to capture stdout and stderr in real-time
        process = subprocess.Popen(
            ["python", "-u", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        logger.info(f"Script stdout: {stdout}")
        logger.error(f"Script stderr: {stderr}")

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error executing script: {stderr}")

        # Return the script output
        return {"result": stdout.strip()}

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
