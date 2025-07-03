# Java Parser Demo Backend

This repository provides a simple backend service for generating JUnit tests
from Java source code. The service exposes a small Flask API that extracts
methods using `javaparser` and generates tests via an LLM.

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

The backend optionally integrates with **LangChain** and **LangSmith** for LLM
invocation and tracing. If these packages are unavailable, the server falls
back to using the raw OpenAI client.

A Java runtime is required for the `ExtractMethod` class. Make sure the
`javaparser-core-3.25.4.jar` is present in the repository.

Set the `OPENAI_API_KEY` environment variable if you want to use the OpenAI
API for generating tests.

## Running the server

```bash
python app.py
```

Send a POST request to `/generate` with JSON containing either `file_path` or
`code`.

Example:

```bash
curl -X POST http://localhost:8000/generate -H 'Content-Type: application/json' \
    -d '{"file_path": "HelloWorld.java"}'
```

The response contains the generated JUnit test.

## Asynchronous generation

You can also start test generation as a background task which can be
cancelled. Use `/start-generate` to begin generation. The response will
include a `task_id` which can be checked via `/status/<task_id>` or
cancelled via `/cancel/<task_id>`.
