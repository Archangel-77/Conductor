"""
CLI for Conductor task queue system.
"""

import asyncio
import sys
from conductor.db.connection import DatabaseConnection
from conductor.db.schema import SchemaManager
from conductor.observability.health import HealthChecker


async def initialize_database():
    """Initialize database schema."""
    try:
        # This would normally come from environment variables
        db_url = "postgresql://user:password@localhost/conductor"
        
        db = DatabaseConnection(db_url)
        await db.connect()
        
        schema = SchemaManager(db)
        await schema.migrate()
        
        print("Database initialized successfully")
        await db.disconnect()
        
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)


async def health_check():
    """Perform health check."""
    try:
        # This would normally come from environment variables
        db_url = "postgresql://user:password@localhost/conductor"
        
        db = DatabaseConnection(db_url)
        await db.connect()
        
        health_checker = HealthChecker(db)
        report = await health_checker.get_health_report()
        
        print(f"Health Status: {report['status']}")
        for check in report['checks']:
            print(f"  {check['component']}: {check['status']} - {check['details']}")
            
        await db.disconnect()
        
    except Exception as e:
        print(f"Failed to perform health check: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: conductor [init|health]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        asyncio.run(initialize_database())
    elif command == "health":
        asyncio.run(health_check())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
