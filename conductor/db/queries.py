"""
Database query builders for Conductor.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import json
from conductor.db.connection import DatabaseConnection
from conductor.core.models import Task, RetryPolicy, Worker, DLQTask, RetryRecord
from conductor.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)


class QueryManager:
    """Manages database queries for Conductor."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    async def insert_task(self, task: Task) -> None:
        """Insert a new task into the database."""
        query = """
        INSERT INTO conductor_tasks (
            task_id, task_type, payload, status, created_at, updated_at,
            worker_id, started_at, completed_at, failed_at, error_message,
            attempts, retry_policy, scheduled_for, route, priority, result
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
        """
        
        try:
            retry_policy_json = json.dumps(task.retry_policy.__dict__) if task.retry_policy else None
            await self.db.execute(query, 
                                task.task_id, task.task_type, task.payload,
                                task.status.value, task.created_at, task.updated_at,
                                task.worker_id, task.started_at, task.completed_at,
                                task.failed_at, task.error_message, task.attempts,
                                retry_policy_json, task.scheduled_for, task.route,
                                task.priority, task.result)
        except Exception as e:
            raise DatabaseError(f"Failed to insert task: {e}")
    
    async def select_pending_tasks(self, limit: int = 10) -> List[Task]:
        """Select pending tasks for processing."""
        query = """
        SELECT task_id, task_type, payload, status, created_at, updated_at,
               worker_id, started_at, completed_at, failed_at, error_message,
               attempts, retry_policy, scheduled_for, route, priority, result
        FROM conductor_tasks 
        WHERE status = 'pending' AND (scheduled_for IS NULL OR scheduled_for <= NOW())
        ORDER BY priority DESC, created_at ASC
        LIMIT $1
        FOR UPDATE SKIP LOCKED
        """
        
        try:
            rows = await self.db.fetch(query, limit)
            tasks = []
            
            for row in rows:
                retry_policy = None
                if row['retry_policy']:
                    policy_data = json.loads(row['retry_policy'])
                    retry_policy = RetryPolicy(**policy_data)
                
                task = Task(
                    task_id=row['task_id'],
                    task_type=row['task_type'],
                    payload=json.loads(row['payload']),
                    status=TaskStatus(row['status']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    worker_id=row['worker_id'],
                    started_at=row['started_at'],
                    completed_at=row['completed_at'],
                    failed_at=row['failed_at'],
                    error_message=row['error_message'],
                    attempts=row['attempts'],
                    retry_policy=retry_policy,
                    scheduled_for=row['scheduled_for'],
                    route=row['route'],
                    priority=row['priority'],
                    result=json.loads(row['result']) if row['result'] else None
                )
                tasks.append(task)
            
            return tasks
        except Exception as e:
            raise DatabaseError(f"Failed to select pending tasks: {e}")
    
    async def update_task_status(self, task_id: str, status: TaskStatus, 
                                worker_id: Optional[str] = None,
                                error_message: Optional[str] = None,
                                result: Optional[Dict] = None) -> None:
        """Update task status."""
        query = """
        UPDATE conductor_tasks 
        SET status = $1, updated_at = NOW(), worker_id = $2, 
            error_message = $3, result = $4
        WHERE task_id = $5
        """
        
        try:
            await self.db.execute(query, status.value, worker_id, error_message, 
                                json.dumps(result) if result else None, task_id)
        except Exception as e:
            raise DatabaseError(f"Failed to update task status: {e}")
    
    async def update_task_started(self, task_id: str, worker_id: str, started_at: datetime) -> None:
        """Update task with start information."""
        query = """
        UPDATE conductor_tasks 
        SET status = 'processing', updated_at = NOW(), worker_id = $1,
            started_at = $2
        WHERE task_id = $3
        """
        
        try:
            await self.db.execute(query, worker_id, started_at, task_id)
        except Exception as e:
            raise DatabaseError(f"Failed to update task start time: {e}")
    
    async def update_task_completed(self, task_id: str, completed_at: datetime, 
                                  result: Optional[Dict] = None) -> None:
        """Update task with completion information."""
        query = """
        UPDATE conductor_tasks 
        SET status = 'completed', updated_at = NOW(), completed_at = $1,
            result = $2
        WHERE task_id = $3
        """
        
        try:
            await self.db.execute(query, completed_at, json.dumps(result) if result else None, task_id)
        except Exception as e:
            raise DatabaseError(f"Failed to update task completion: {e}")
    
    async def update_task_failed(self, task_id: str, failed_at: datetime, 
                               error_message: str) -> None:
        """Update task with failure information."""
        query = """
        UPDATE conductor_tasks 
        SET status = 'failed', updated_at = NOW(), failed_at = $1,
            error_message = $2
        WHERE task_id = $3
        """
        
        try:
            await self.db.execute(query, failed_at, error_message, task_id)
        except Exception as e:
            raise DatabaseError(f"Failed to update task failure: {e}")
    
    async def insert_retry_record(self, retry_record: RetryRecord) -> None:
        """Insert a retry record."""
        query = """
        INSERT INTO conductor_retries (
            task_id, attempt_number, error_message, retry_at, created_at
        ) VALUES ($1, $2, $3, $4, $5)
        """
        
        try:
            await self.db.execute(query, retry_record.task_id, retry_record.attempt_number,
                                retry_record.error_message, retry_record.retry_at,
                                retry_record.created_at)
        except Exception as e:
            raise DatabaseError(f"Failed to insert retry record: {e}")
    
    async def move_to_dlq(self, task: Task, error_message: str) -> None:
        """Move a failed task to dead letter queue."""
        query = """
        INSERT INTO conductor_dead_letter (
            task_id, task_type, payload, error_message, last_error_at,
            attempts, created_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        
        try:
            await self.db.execute(query, task.task_id, task.task_type,
                                json.dumps(task.payload), error_message,
                                task.failed_at, task.attempts, task.created_at)
        except Exception as e:
            raise DatabaseError(f"Failed to move task to DLQ: {e}")
    
    async def select_dlq_tasks(self, limit: int = 10) -> List[DLQTask]:
        """Select tasks from dead letter queue."""
        query = """
        SELECT task_id, task_type, payload, error_message, last_error_at,
               attempts, created_at, discarded_at, discard_reason
        FROM conductor_dead_letter 
        ORDER BY created_at DESC
        LIMIT $1
        """
        
        try:
            rows = await self.db.fetch(query, limit)
            dlq_tasks = []
            
            for row in rows:
                dlq_task = DLQTask(
                    task_id=row['task_id'],
                    task_type=row['task_type'],
                    payload=json.loads(row['payload']),
                    error_message=row['error_message'],
                    last_error_at=row['last_error_at'],
                    attempts=row['attempts'],
                    created_at=row['created_at'],
                    discarded_at=row['discarded_at'],
                    discard_reason=row['discard_reason']
                )
                dlq_tasks.append(dlq_task)
            
            return dlq_tasks
        except Exception as e:
            raise DatabaseError(f"Failed to select DLQ tasks: {e}")
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        query = """
        SELECT task_id, task_type, payload, status, created_at, updated_at,
               worker_id, started_at, completed_at, failed_at, error_message,
               attempts, retry_policy, scheduled_for, route, priority, result
        FROM conductor_tasks 
        WHERE task_id = $1
        """
        
        try:
            row = await self.db.fetch_one(query, task_id)
            if not row:
                return None
                
            retry_policy = None
            if row['retry_policy']:
                policy_data = json.loads(row['retry_policy'])
                retry_policy = RetryPolicy(**policy_data)
            
            return Task(
                task_id=row['task_id'],
                task_type=row['task_type'],
                payload=json.loads(row['payload']),
                status=TaskStatus(row['status']),
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                worker_id=row['worker_id'],
                started_at=row['started_at'],
                completed_at=row['completed_at'],
                failed_at=row['failed_at'],
                error_message=row['error_message'],
                attempts=row['attempts'],
                retry_policy=retry_policy,
                scheduled_for=row['scheduled_for'],
                route=row['route'],
                priority=row['priority'],
                result=json.loads(row['result']) if row['result'] else None
            )
        except Exception as e:
            raise DatabaseError(f"Failed to get task: {e}")
    
    async def select_worker_by_id(self, worker_id: str) -> Optional[Worker]:
        """Get a specific worker by ID."""
        query = """
        SELECT worker_id, hostname, pid, status, started_at, last_heartbeat,
               tasks_processed_total, tasks_failed_total, current_task_id, uptime_seconds
        FROM conductor_workers 
        WHERE worker_id = $1
        """
        
        try:
            row = await self.db.fetch_one(query, worker_id)
            if not row:
                return None
                
            return Worker(
                worker_id=row['worker_id'],
                hostname=row['hostname'],
                pid=row['pid'],
                status=row['status'],
                started_at=row['started_at'],
                last_heartbeat=row['last_heartbeat'],
                tasks_processed_total=row['tasks_processed_total'],
                tasks_failed_total=row['tasks_failed_total'],
                current_task_id=row['current_task_id'],
                uptime_seconds=row['uptime_seconds']
            )
        except Exception as e:
            raise DatabaseError(f"Failed to get worker: {e}")
    
    async def insert_worker(self, worker: Worker) -> None:
        """Insert a new worker."""
        query = """
        INSERT INTO conductor_workers (
            worker_id, hostname, pid, status, started_at, last_heartbeat,
            tasks_processed_total, tasks_failed_total, current_task_id, uptime_seconds
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """
        
        try:
            await self.db.execute(query, worker.worker_id, worker.hostname, worker.pid,
                                worker.status, worker.started_at, worker.last_heartbeat,
                                worker.tasks_processed_total, worker.tasks_failed_total,
                                worker.current_task_id, worker.uptime_seconds)
        except Exception as e:
            raise DatabaseError(f"Failed to insert worker: {e}")
    
    async def update_worker_heartbeat(self, worker_id: str, last_heartbeat: datetime) -> None:
        """Update worker heartbeat."""
        query = """
        UPDATE conductor_workers 
        SET last_heartbeat = $1
        WHERE worker_id = $2
        """
        
        try:
            await self.db.execute(query, last_heartbeat, worker_id)
        except Exception as e:
            raise DatabaseError(f"Failed to update worker heartbeat: {e}")
