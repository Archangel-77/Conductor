"""
Test cases for Conductor models.
"""

import pytest
from datetime import datetime
from conductor.core.models import Task, TaskStatus, RetryPolicy, Worker


def test_task_creation():
    """Test Task model creation."""
    task = Task(
        task_id="test-task-123",
        task_type="email_notification",
        payload={"to": "user@example.com", "subject": "Hello"},
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert task.task_id == "test-task-123"
    assert task.task_type == "email_notification"
    assert task.status == TaskStatus.PENDING
    assert task.payload == {"to": "user@example.com", "subject": "Hello"}


def test_retry_policy():
    """Test RetryPolicy model."""
    policy = RetryPolicy(
        max_retries=5,
        backoff="exponential",
        initial_delay=2.0,
        max_delay=3600.0
    )
    
    assert policy.max_retries == 5
    assert policy.backoff == "exponential"
    assert policy.initial_delay == 2.0
    assert policy.max_delay == 3600.0


def test_worker_creation():
    """Test Worker model creation."""
    worker = Worker(
        worker_id="worker-456",
        hostname="test-host",
        pid=12345,
        status="idle",
        started_at=datetime.now(),
        last_heartbeat=datetime.now()
    )
    
    assert worker.worker_id == "worker-456"
    assert worker.hostname == "test-host"
    assert worker.pid == 12345
    assert worker.status == "idle"


def test_task_status_enum():
    """Test TaskStatus enum values."""
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.PROCESSING.value == "processing"
    assert TaskStatus.COMPLETED.value == "completed"
    assert TaskStatus.FAILED.value == "failed"
    assert TaskStatus.RETRYING.value == "retrying"
