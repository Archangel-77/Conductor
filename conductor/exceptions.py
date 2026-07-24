"""
Custom exceptions for Conductor task queue system.
"""

class ConductorException(Exception):
    """Base exception for all Conductor errors."""
    pass


class DatabaseError(ConductorException):
    """Raised when database operations fail."""
    pass


class WorkerError(ConductorException):
    """Raised when worker operations fail."""
    pass


class TaskError(ConductorException):
    """Raised when task operations fail."""
    pass


class RetryPolicyError(ConductorException):
    """Raised when retry policy validation fails."""
    pass


class ConnectionError(ConductorException):
    """Raised when database connection fails."""
    pass
