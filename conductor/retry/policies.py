"""
Retry policies for Conductor task queue system.
"""

from typing import Optional, Dict, Any
from conductor.core.models import RetryPolicy
from conductor.exceptions import RetryPolicyError
import time
import random


class RetryPolicyManager:
    """Manages retry policy logic for tasks."""
    
    @staticmethod
    def calculate_delay(policy: RetryPolicy, attempt_number: int) -> float:
        """
        Calculate delay before next retry based on policy.
        
        Args:
            policy: The retry policy to use
            attempt_number: Which attempt this is (1-based)
            
        Returns:
            Delay in seconds
        """
        if attempt_number > policy.max_retries:
            raise RetryPolicyError("Attempt number exceeds max retries")
        
        if policy.backoff == "exponential":
            delay = policy.initial_delay * (2 ** (attempt_number - 1))
        elif policy.backoff == "linear":
            delay = policy.initial_delay * attempt_number
        elif policy.backoff == "fixed":
            delay = policy.initial_delay
        else:
            raise RetryPolicyError(f"Unknown backoff type: {policy.backoff}")
        
        # Cap the delay at max_delay
        return min(delay, policy.max_delay)
    
    @staticmethod
    def should_retry(policy: RetryPolicy, attempt_number: int) -> bool:
        """
        Determine if a task should be retried.
        
        Args:
            policy: The retry policy to use
            attempt_number: Which attempt this is (1-based)
            
        Returns:
            True if the task should be retried, False otherwise
        """
        return attempt_number <= policy.max_retries
    
    @staticmethod
    def get_default_retry_policy() -> RetryPolicy:
        """Get a default retry policy."""
        return RetryPolicy(
            max_retries=3,
            backoff="exponential",
            initial_delay=1.0,
            max_delay=3600.0  # 1 hour
        )
