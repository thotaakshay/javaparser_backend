import threading
import uuid
from typing import Dict, Any

from junit_test_generator import generate_junit_test


class TaskInfo:
    def __init__(self, thread: threading.Thread, cancel_event: threading.Event, result: Dict[str, Any]):
        self.thread = thread
        self.cancel_event = cancel_event
        self.result = result


tasks: Dict[str, TaskInfo] = {}


def start_generation(method_code: str) -> str:
    task_id = str(uuid.uuid4())
    cancel_event = threading.Event()
    result: Dict[str, Any] = {"status": "running", "junit_test": None}

    def run():
        if cancel_event.is_set():
            result["status"] = "cancelled"
            return
        junit = generate_junit_test(method_code, cancel_event=cancel_event)
        if cancel_event.is_set():
            result["status"] = "cancelled"
            return
        result["junit_test"] = junit
        result["status"] = "completed"

    thread = threading.Thread(target=run, daemon=True)
    tasks[task_id] = TaskInfo(thread, cancel_event, result)
    thread.start()
    return task_id


def cancel_task(task_id: str) -> bool:
    info = tasks.get(task_id)
    if not info:
        return False
    info.cancel_event.set()
    return True


def get_status(task_id: str) -> Dict[str, Any]:
    info = tasks.get(task_id)
    if not info:
        return {"status": "unknown"}
    return info.result
