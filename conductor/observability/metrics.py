"""
Metrics collection for Conductor task queue system.
"""

from typing import Dict, Any
import time
from prometheus_client import Counter, Histogram, Gauge
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects and exposes metrics for Conductor."""
    
    def __init__(self):
        # Task-related counters
        self.tasks_created = Counter(
            'conductor_tasks_created_total',
            'Total number of tasks created',
            ['task_type']
        )
        
        self.tasks_processed = Counter(
            'conductor_tasks_processed_total',
            'Total number of tasks processed',
            ['task_type', 'status']
        )
        
        self.tasks_failed = Counter(
            'conductor_tasks_failed_total',
            'Total number of failed tasks',
            ['task_type']
        )
        
        self.tasks_retried = Counter(
            'conductor_tasks_retried_total',
            'Total number of task retries',
            ['task_type']
        )
        
        # Task duration histogram
        self.task_duration = Histogram(
            'conductor_task_duration_seconds',
            'Task execution duration',
            ['task_type']
        )
        
        # Worker metrics
        self.workers_registered = Gauge(
            'conductor_workers_registered',
            'Number of registered workers'
        )
        
        self.workers_active = Gauge(
            'conductor_workers_active',
            'Number of active workers'
        )
        
        self.tasks_in_queue = Gauge(
            'conductor_tasks_in_queue',
            'Number of tasks in queue',
            ['status']
        )
    
    def task_started(self, task_type: str) -> None:
        """Record that a task has started processing."""
        self.tasks_created.labels(task_type=task_type).inc()
    
    def task_completed(self, task_type: str, duration: float) -> None:
        """Record that a task has completed successfully."""
        self.tasks_processed.labels(task_type=task_type, status='completed').inc()
        self.task_duration.labels(task_type=task_type).observe(duration)
    
    def task_failed(self, task_type: str) -> None:
        """Record that a task has failed."""
        self.tasks_processed.labels(task_type=task_type, status='failed').inc()
        self.tasks_failed.labels(task_type=task_type).inc()
    
    def task_retried(self, task_type: str) -> None:
        """Record that a task has been retried."""
        self.tasks_retried.labels(task_type=task_type).inc()
    
    def worker_registered(self, count: int = 1) -> None:
        """Record worker registration."""
        self.workers_registered.inc(count)
    
    def worker_unregistered(self, count: int = 1) -> None:
        """Record worker unregistration."""
        self.workers_registered.dec(count)
    
    def worker_active(self, count: int = 1) -> None:
        """Record active workers."""
        self.workers_active.inc(count)
    
    def worker_inactive(self, count: int = 1) -> None:
        """Record inactive workers."""
        self.workers_active.dec(count)
    
    def queue_size(self, status: str, size: int) -> None:
        """Record queue size for a specific status."""
        self.tasks_in_queue.labels(status=status).set(size)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics as dictionary."""
        return {
            'tasks_created': self.tasks_created._metrics,
            'tasks_processed': self.tasks_processed._metrics,
            'tasks_failed': self.tasks_failed._metrics,
            'tasks_retried': self.tasks_retried._metrics,
            'task_duration': self.task_duration._metrics,
            'workers_registered': self.workers_registered._metrics,
            'workers_active': self.workers_active._metrics,
            'tasks_in_queue': self.tasks_in_queue._metrics
        }
