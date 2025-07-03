from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import os
import zipfile

from extract_method import extract_method
from junit_test_generator import generate_junit_test
from task_manager import start_generation, cancel_task, get_status

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_request_data(request: Request):
    if request.headers.get("content-type", "").startswith("application/json"):
        return request.json()
    return request.form()


@app.post("/generate")
async def generate(request: Request):
    data = await _get_request_data(request)
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    java_file = None
    if data.get("code"):
        java_file = "TempInput.java"
        with open(java_file, "w") as f:
            f.write(data["code"])
    elif data.get("file_path"):
        java_file = data["file_path"]
    else:
        raise HTTPException(status_code=400, detail="Provide code or file_path")

    method_code = extract_method(java_file)
    if method_code is None:
        raise HTTPException(status_code=500, detail="Failed to extract method")

    junit_test = generate_junit_test(method_code)
    return JSONResponse({"junit_test": junit_test})


@app.post("/start-generate")
async def start_generate(request: Request):
    data = await _get_request_data(request)
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    java_file = None
    if data.get("code"):
        java_file = "TempInput.java"
        with open(java_file, "w") as f:
            f.write(data["code"])
    elif data.get("file_path"):
        java_file = data["file_path"]
    else:
        raise HTTPException(status_code=400, detail="Provide code or file_path")

    method_code = extract_method(java_file)
    if method_code is None:
        raise HTTPException(status_code=500, detail="Failed to extract method")

    task_id = start_generation(method_code)
    return JSONResponse({"task_id": task_id})


@app.get("/status/{task_id}")
async def status(task_id: str):
    return JSONResponse(get_status(task_id))


@app.post("/cancel/{task_id}")
async def cancel(task_id: str):
    if cancel_task(task_id):
        return JSONResponse({"status": "cancelling"})
    raise HTTPException(status_code=404, detail="unknown task")


@app.post("/generate-tests")
async def generate_tests(request: Request):
    data = await _get_request_data(request)
    if not data or "files" not in data:
        raise HTTPException(status_code=400, detail="No files provided")

    files = data["files"]
    if not isinstance(files, list):
        raise HTTPException(status_code=400, detail="files must be a list")

    test_files = {}
    for file in files:
        name = file.get("name")
        content = file.get("content")
        if not name or content is None:
            continue
        junit = generate_junit_test(content)
        test_name = name.rsplit('.', 1)[0] + 'Test.java'
        test_files[test_name] = junit

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for fname, code in test_files.items():
            zf.writestr(fname, code)
    mem_zip.seek(0)
    return StreamingResponse(
        mem_zip,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=junit-tests.zip"},
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
