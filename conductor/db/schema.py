"""
Database schema management for Conductor.
"""

import asyncio
from typing import List, Dict, Any
from conductor.db.connection import DatabaseConnection
from conductor.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema creation and migrations."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    async def create_schema_version_table(self) -> None:
        """Create schema version tracking table."""
        query = """
        CREATE TABLE IF NOT EXISTS conductor_version (
            version INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        try:
            await self.db.execute(query)
            logger.info("Schema version table created")
        except Exception as e:
            raise DatabaseError(f"Failed to create schema version table: {e}")
    
    async def get_schema_version(self) -> int:
        """Get current schema version."""
        query = "SELECT version FROM conductor_version ORDER BY version DESC LIMIT 1;"
        try:
            result = await self.db.fetch_one(query)
            return result['version'] if result else 0
        except Exception as e:
            logger.warning(f"Could not get schema version: {e}")
            return 0
    
    async def create_tables(self) -> None:
        """Create all required tables."""
        # Create version table first
        await self.create_schema_version_table()
        
        # Create tasks table
        tasks_query = """
        CREATE TABLE IF NOT EXISTS conductor_tasks (
            task_id VARCHAR(36) PRIMARY KEY,
            task_type VARCHAR(255) NOT NULL,
            payload TEXT NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            worker_id VARCHAR(36),
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            failed_at TIMESTAMP,
            error_message TEXT,
            attempts INTEGER DEFAULT 0,
            retry_policy TEXT,
            scheduled_for TIMESTAMP,
            route VARCHAR(100) DEFAULT 'default',
            priority INTEGER DEFAULT 0,
            result TEXT,
            INDEX idx_task_type (task_type),
            INDEX idx_status (status),
            INDEX idx_worker_id (worker_id),
            INDEX idx_scheduled_for (scheduled_for),
            INDEX idx_route (route),
            INDEX idx_priority (priority)
        );
        """
        
        # Create workers table
        workers_query = """
        CREATE TABLE IF NOT EXISTS conductor_workers (
            worker_id VARCHAR(36) PRIMARY KEY,
            hostname VARCHAR(255) NOT NULL,
            pid INTEGER NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'idle',
            started_at TIMESTAMP DEFAULT NOW(),
            last_heartbeat TIMESTAMP DEFAULT NOW(),
            tasks_processed_total INTEGER DEFAULT 0,
            tasks_failed_total INTEGER DEFAULT 0,
            current_task_id VARCHAR(36),
            uptime_seconds INTEGER DEFAULT 0,
            INDEX idx_status (status),
            INDEX idx_hostname (hostname)
        );
        """
        
        # Create retries table
        retries_query = """
        CREATE TABLE IF NOT EXISTS conductor_retries (
            id SERIAL PRIMARY KEY,
            task_id VARCHAR(36) NOT NULL,
            attempt_number INTEGER NOT NULL,
            error_message TEXT,
            retry_at TIMESTAMP DEFAULT NOW(),
            created_at TIMESTAMP DEFAULT NOW(),
            INDEX idx_task_id (task_id),
            INDEX idx_attempt (attempt_number)
        );
        """
        
        # Create dead letter queue table
        dlq_query = """
        CREATE TABLE IF NOT EXISTS conductor_dead_letter (
            task_id VARCHAR(36) PRIMARY KEY,
            task_type VARCHAR(255) NOT NULL,
            payload TEXT NOT NULL,
            error_message TEXT NOT NULL,
            last_error_at TIMESTAMP DEFAULT NOW(),
            attempts INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW(),
            discarded_at TIMESTAMP,
            discard_reason TEXT,
            INDEX idx_task_type (task_type),
            INDEX idx_created_at (created_at)
        );
        """
        
        # Create recurring tasks table (for future use)
        recurring_query = """
        CREATE TABLE IF NOT EXISTS conductor_recurring_tasks (
            id SERIAL PRIMARY KEY,
            task_type VARCHAR(255) NOT NULL,
            cron_expression VARCHAR(100) NOT NULL,
            payload TEXT NOT NULL,
            enabled BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            next_run_at TIMESTAMP,
            INDEX idx_task_type (task_type),
            INDEX idx_enabled (enabled)
        );
        """
        
        try:
            await self.db.execute(tasks_query)
            await self.db.execute(workers_query)
            await self.db.execute(retries_query)
            await self.db.execute(dlq_query)
            await self.db.execute(recurring_query)
            
            # Insert initial schema version
            version_check = "SELECT 1 FROM conductor_version WHERE version = 1;"
            result = await self.db.fetch_one(version_check)
            
            if not result:
                insert_query = "INSERT INTO conductor_version (version) VALUES (1);"
                await self.db.execute(insert_query)
                
            logger.info("All database tables created successfully")
        except Exception as e:
            raise DatabaseError(f"Failed to create database tables: {e}")
    
    async def migrate(self) -> None:
        """Run all migrations."""
        current_version = await self.get_schema_version()
        
        if current_version < 1:
            logger.info("Running initial schema migration")
            await self.create_tables()
            logger.info("Initial schema migration completed")
