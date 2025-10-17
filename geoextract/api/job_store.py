"""In-memory job storage shared across API modules."""

from __future__ import annotations

from copy import deepcopy
from threading import Lock
from typing import Any, Dict, List, Optional

_lock = Lock()
_jobs: Dict[str, Dict[str, Any]] = {}


def create_job(job_id: str, data: Dict[str, Any]) -> None:
    """Create a new job entry."""

    with _lock:
        _jobs[job_id] = deepcopy(data)


def set_job(job_id: str, data: Dict[str, Any]) -> None:
    """Replace job data, creating it if necessary."""

    with _lock:
        _jobs[job_id] = deepcopy(data)


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve job data by ID."""

    with _lock:
        job = _jobs.get(job_id)
        return deepcopy(job) if job is not None else None


def list_jobs() -> List[Dict[str, Any]]:
    """List all jobs."""

    with _lock:
        return [deepcopy(job) for job in _jobs.values()]


def update_job(job_id: str, **updates: Any) -> Dict[str, Any]:
    """Update fields for a job."""

    with _lock:
        if job_id not in _jobs:
            raise KeyError(f"Job {job_id} not found")
        _jobs[job_id].update(updates)
        return deepcopy(_jobs[job_id])


def delete_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Delete a job and return its data."""

    with _lock:
        job = _jobs.pop(job_id, None)
        return deepcopy(job) if job is not None else None


def job_exists(job_id: str) -> bool:
    """Return True if a job exists."""

    with _lock:
        return job_id in _jobs
