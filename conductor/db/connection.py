"""
Database connection management for Conductor.
"""

import asyncio
import asyncpg
from typing import Optional, Dict, Any
from conductor.exceptions import ConnectionError
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages PostgreSQL connection pool for Conductor."""
    
    def __init__(
        self,
        database_url: str,
        min_size: int = 10,
        max_size: int = 20,
        timeout: float = 60.0
    ):
        self.database_url = database_url
        self.min_size = min_size
        self.max_size = max_size
        self.timeout = timeout
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """Establish connection pool to PostgreSQL."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=self.timeout
            )
            logger.info("Database connection established")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    async def disconnect(self) -> None:
        """Close all database connections."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connections closed")
    
    async def health_check(self) -> bool:
        """Check if database is reachable."""
        if not self.pool:
            return False
        
        try:
            conn = await self.pool.acquire()
            try:
                await conn.fetchval('SELECT 1')
                return True
            finally:
                await self.pool.release(conn)
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def execute(self, query: str, *args) -> Any:
        """Execute a query."""
        if not self.pool:
            raise ConnectionError("Database pool not initialized")
        
        conn = await self.pool.acquire()
        try:
            result = await conn.execute(query, *args)
            return result
        finally:
            await self.pool.release(conn)
    
    async def fetch(self, query: str, *args) -> Any:
        """Fetch one row from database."""
        if not self.pool:
            raise ConnectionError("Database pool not initialized")
        
        conn = await self.pool.acquire()
        try:
            result = await conn.fetch(query, *args)
            return result
        finally:
            await self.pool.release(conn)
    
    async def fetch_one(self, query: str, *args) -> Any:
        """Fetch one row from database."""
        if not self.pool:
            raise ConnectionError("Database pool not initialized")
        
        conn = await self.pool.acquire()
        try:
            result = await conn.fetchrow(query, *args)
            return result
        finally:
            await self.pool.release(conn)
