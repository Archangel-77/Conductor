"""
Health check implementation for Conductor task queue system.
"""

import asyncio
from typing import Dict, Any, List
from conductor.db.connection import DatabaseConnection
from conductor.exceptions import ConnectionError
import logging

logger = logging.getLogger(__name__)


class HealthChecker:
    """Performs health checks for Conductor components."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and health."""
        try:
            is_healthy = await self.db.health_check()
            return {
                'status': 'healthy' if is_healthy else 'unhealthy',
                'component': 'database',
                'details': 'Connected to PostgreSQL' if is_healthy else 'Failed to connect'
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'component': 'database',
                'details': f'Error during health check: {str(e)}'
            }
    
    async def check_all(self) -> List[Dict[str, Any]]:
        """Perform all health checks."""
        results = []
        
        # Check database
        db_result = await self.check_database()
        results.append(db_result)
        
        return results
    
    async def get_health_report(self) -> Dict[str, Any]:
        """Get a complete health report."""
        checks = await self.check_all()
        overall_status = 'healthy' if all(check['status'] == 'healthy' for check in checks) else 'unhealthy'
        
        return {
            'status': overall_status,
            'checks': checks,
            'timestamp': asyncio.get_event_loop().time()
        }
