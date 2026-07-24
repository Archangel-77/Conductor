"""
Backoff strategies for Conductor task queue system.
"""

import time
import random
from typing import Union


class BackoffStrategy:
    """Base backoff strategy class."""
    
    def __init__(self, initial_delay: float = 1.0, max_delay: float = 3600.0):
        self.initial_delay = initial_delay
        self.max_delay = max_delay
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given attempt."""
        raise NotImplementedError


class ExponentialBackoff(BackoffStrategy):
    """Exponential backoff strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        delay = self.initial_delay * (2 ** (attempt - 1))
        return min(delay, self.max_delay)


class LinearBackoff(BackoffStrategy):
    """Linear backoff strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        delay = self.initial_delay * attempt
        return min(delay, self.max_delay)


class FixedBackoff(BackoffStrategy):
    """Fixed backoff strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        return self.initial_delay


class JitteredExponentialBackoff(BackoffStrategy):
    """Exponential backoff with jitter."""
    
    def calculate_delay(self, attempt: int) -> float:
        delay = self.initial_delay * (2 ** (attempt - 1))
        # Add jitter (±25%)
        jitter = random.uniform(-0.25, 0.25) * delay
        delay = min(delay + jitter, self.max_delay)
        return max(delay, self.initial_delay)
