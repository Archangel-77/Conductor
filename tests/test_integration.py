"""
Integration tests for Conductor components.
"""

import pytest
import asyncio
from datetime import datetime
from conductor.core.models import Task, TaskStatus, RetryPolicy
from conductor.db.connection import DatabaseConnection
from conductor.db.queries import QueryManager
from conductor.utils import generate_task_id


@pytest.mark.asyncio
async def test_task_model_creation():
    """Test that Task model can be created properly."""
    task = Task(
        task_id=generate_task_id(),
        task_type="test_task",
        payload={"key": "value"},
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    assert task.task_id is not None
    assert task.task_type == "test_task"
    assert task.payload == {"key": "value"}
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_retry_policy_creation():
    """Test that RetryPolicy model can be created properly."""
    policy = RetryPolicy(
        max_retries=3,
        backoff="exponential",
        initial_delay=1.0,
        max_delay=3600.0
    )
    
    assert policy.max_retries == 3
    assert policy.backoff == "exponential"
    assert policy.initial_delay == 1.0
    assert policy.max_delay == 3600.0


def test_model_imports():
    """Test that all core models can be imported."""
    from conductor.core.models import Task, TaskStatus, RetryPolicy, Worker, DLQTask
    
    # Test all imports work
    assert Task is not None
    assert TaskStatus is not None
    assert RetryPolicy is not None
    assert Worker is not None
    assert DLQTask is not None


def test_utils_functions():
    """Test utility functions."""
    from conductor.utils import generate_task_id, get_current_timestamp
    
    # Test ID generation
    task_id = generate_task_id()
    assert isinstance(task_id, str)
    assert len(task_id) > 0
    
    # Test timestamp
    timestamp = get_current_timestamp()
    assert timestamp is not None
    assert isinstance(timestamp, datetime)
