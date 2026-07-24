"""
Data models for Conductor task queue system.
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class RetryPolicy:
    """Retry policy configuration for tasks."""
    max_retries: int = 3
    backoff: str = "exponential"  # exponential, linear, fixed
    initial_delay: float = 1.0  # seconds
    max_delay: float = 3600.0   # seconds


@dataclass
class Task:
    """Task model representing a unit of work."""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    worker_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    attempts: int = 0
    retry_policy: Optional[RetryPolicy] = None
    scheduled_for: Optional[datetime] = None
    route: str = "default"
    priority: int = 0
    result: Optional[Dict[str, Any]] = None


@dataclass
class Worker:
    """Worker model representing a task processor."""
    worker_id: str
    hostname: str
    pid: int
    status: str  # idle, processing, unhealthy
    started_at: datetime
    last_heartbeat: datetime
    tasks_processed_total: int = 0
    tasks_failed_total: int = 0
    current_task_id: Optional[str] = None
    uptime_seconds: int = 0


@dataclass
class RetryRecord:
    """Record of a retry attempt."""
    task_id: str
    attempt_number: int
    error_message: Optional[str]
    retry_at: datetime
    created_at: datetime


@dataclass
class DLQTask:
    """Task that has failed all retries and is in dead letter queue."""
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    error_message: str
    last_error_at: datetime
    attempts: int
    created_at: datetime
    discarded_at: Optional[datetime] = None
    discard_reason: Optional[str] = None
