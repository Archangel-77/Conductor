"""
Utility functions for Conductor task queue system.
"""

import uuid
from datetime import datetime
import json
import os


def generate_task_id() -> str:
    """Generate a unique task ID."""
    return str(uuid.uuid4())


def generate_correlation_id() -> str:
    """Generate a correlation ID for request tracking."""
    return str(uuid.uuid4())


def serialize_payload(payload: dict) -> str:
    """Serialize payload to JSON string."""
    try:
        return json.dumps(payload)
    except Exception as e:
        raise ValueError(f"Failed to serialize payload: {e}")


def deserialize_payload(payload_str: str) -> dict:
    """Deserialize JSON string to dictionary."""
    try:
        return json.loads(payload_str)
    except Exception as e:
        raise ValueError(f"Failed to deserialize payload: {e}")


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()


def get_hostname() -> str:
    """Get hostname of the system."""
    return os.uname().nodename if hasattr(os, 'uname') else 'unknown'


def get_pid() -> int:
    """Get process ID."""
    return os.getpid()
