# Conductor

A robust task queue system with database persistence, retry logic, and observability.

## Features

- Database-backed task queue
- Retry policies with exponential backoff
- Dead letter queue for failed tasks
- Prometheus metrics and logging
- Priority queues and task routing
- Worker heartbeats and health checks

## Installation

```bash
pip install .
```

## Quick Start

```python
from conductor.core.models import Task
from conductor.db.connection import get_db_connection

# Create a task
task = Task(
    id="task-1",
    name="example-task",
    payload={"data": "example"},
    status="pending"
)

# Submit task to queue
async with get_db_connection() as conn:
    await conn.execute("INSERT INTO conductor_tasks VALUES ($1, $2, $3, $4, $5, $6)", 
                       task.id, task.name, task.payload, task.status, task.created_at, task.updated_at)
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
```
