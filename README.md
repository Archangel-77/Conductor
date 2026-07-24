# Conductor

A robust, production-grade async task queue system built with Python and PostgreSQL. This open-source project is designed to solve a real problem that every backend engineering team encounters - rebuilding task queue functionality from scratch.

## Why This Project?

This project serves as both a practical solution to a common engineering challenge and a demonstration of production-grade software engineering skills for job seekers. It addresses the gap between simple task queues (like RQ) and over-engineered solutions (like Celery), providing a clean, reliable alternative with SQL persistence.

### The Problem
Every Python team that outgrows Celery or doesn't want Redis dependency rebuilds task queue logic. Current solutions are either:
- Over-engineered (Celery)
- Too simple (RQ)

### Why It Gets You Hired
✓ Core strengths: async architecture, reliability patterns, production discipline  
✓ Solves a real problem every backend team encounters  
✓ Community engagement (not just portfolio projects)  
✓ Technical leadership signal  

## Project Overview

This is a 6-month open-source project designed to build a complete async task queue system that demonstrates production-grade engineering skills for job applications. The project addresses a real pain point in backend engineering teams and showcases your ability to ship production-quality software.

### Key Design Principles
1. **Exactly-Once Semantics**: Tasks execute once even if workers crash. Idempotency required.
2. **No External Dependencies**: PostgreSQL only. Deploy anywhere.
3. **Observable from Day One**: Structured logging, metrics, health endpoints.
4. **Graceful Failure**: Retry logic, dead letter queues, operator control.
5. **Simple API**: One function to submit tasks. No learning curve.

## 6-Month Development Plan

### Phase 1 (Months 1-2): Foundation
**Goal**: Build core async task queue with SQL persistence, retry logic, and clean API.

#### Month 1-2: Foundation Phase
- **Week 1-2**: Architecture & Design
  - Define API: task definition, task submission, worker registration
  - Design schema: PostgreSQL tables for tasks, workers, retries, dead letters
  - Plan observability: logging structure, metrics hooks, health checks
  - Write architecture doc explaining design choices

- **Week 3-4**: Core Implementation
  - Task producer: submit task → store in DB → enqueue for processing
  - Worker pool: async worker threads, graceful shutdown, health heartbeat
  - Retry logic: exponential backoff, max retries, circuit breaker
  - SQL persistence: PostgreSQL backend (no in-memory dependency)

- **Week 5-6**: Testing & Polish
  - Test suite: happy path, failures, retries, graceful shutdown
  - Type hints throughout (mypy strict mode)
  - Docker: Dockerfile + docker-compose for local dev
  - Example: FastAPI + simple task

- **Week 7-8**: Launch & Documentation
  - Comprehensive README with architecture diagram
  - Comparison doc: vs Celery, RQ, dramatiq
  - GitHub Actions CI: lint, type check, test, coverage
  - Publish to PyPI v0.1.0

### Phase 2 (Months 2-3): Features & Content
**Goal**: Add production features, create content that attracts users and hiring attention.

#### Month 2-3: Features & Content Phase
- **Week 1-2**: Production Features
  - Dead letter queue for failed tasks
  - Task routing to specific worker pools
  - Priority queues
  - Scheduled tasks (cron-like)

- **Week 3-4**: Observability & Examples
  - Built-in metrics: counts, latency, error rates (Prometheus-compatible)
  - Structured logging: JSON correlation with task IDs
  - 3+ examples: FastAPI, Django, standalone

### Phase 3 (Months 4-5): Growth & Visibility
**Goal**: Drive adoption and position yourself as creator of a credible tool.

#### Month 4-5: Growth & Visibility Phase
- Community Outreach:
  - Hacker News: 'Show HN: A task queue for Python teams'
  - Reddit r/Python: Thoughtful discussion, respond to questions
  - Python Slack communities: Share in #projects
  - Direct outreach: 10-15 FastAPI/async teams for feedback
  - Benchmarks: Performance vs Celery/RQ (honest numbers)

- Metrics to Aim For:
  - 500-1000 GitHub stars
  - 100+ PyPI downloads per week
  - 20-30 issues/comments (active community)
  - 5-6 blog posts published

### Phase 4 (Month 6): Hiring Positioning
**Goal**: Prepare hiring narrative and apply to roles.

#### Month 6: HIRING POSITIONING PHASE
- **Your Story**: I identified a recurring pattern: every Python team rebuilds async task queue logic when Celery becomes too much or Redis is unavailable. I built an open-source solution adopted by 100+ teams.
- Visibility Activities:
  - Update LinkedIn: mention project, link GitHub
  - Post retrospective: 'Lessons from 6 months building open-source'
  - Create case study (optional SaaS variant)
- Job Applications:
  - Target: Backend Engineer, Infrastructure, Systems Engineer roles
  - Target companies: Stripe, Figma, Linear, Discord, Mercury
  - Pitch: Link project in resume/cover letter

## Core Features Implemented (Phase 1 Sprint 1)

### Database & Schema
- PostgreSQL connection pool using asyncpg
- Complete database schema with migrations
- Auto-migration on startup
- All required tables created with proper indexes:
  - `conductor_tasks`: Task lifecycle management
  - `conductor_workers`: Worker status and health monitoring  
  - `conductor_retries`: Retry history tracking
  - `conductor_dead_letter`: Failed tasks that couldn't be retried

### Data Models & Types
- Task, Worker, RetryPolicy, RetryRecord, DLQTask data models
- Pydantic validation and type hints throughout
- Proper serialization/deserialization methods

### Core Functionality
- Task producer: submit task → store in DB → enqueue for processing
- Worker pool: async worker threads with graceful shutdown and health heartbeat
- Retry logic: exponential backoff, max retries, circuit breaker
- Dead letter queue for failed tasks that can't be retried

### Observability & Monitoring
- Structured logging with JSON format and correlation IDs
- Prometheus-compatible metrics collection
- Health check endpoints
- Comprehensive logging for all task state transitions

## Technical Stack

Python 3.11+ | FastAPI (optional HTTP) | asyncio + aiohttp | PostgreSQL + SQLAlchemy async + Alembic | Python logging (JSON) + Prometheus hooks | pytest + pytest-asyncio (85%+ coverage) | Docker + GitHub Actions

## Getting Started

```bash
# Install the package in development mode
pip install -e .

# Run tests
pytest

# Format code with black
black .

# Type check with mypy
mypy .
```

## Development Practices

This project follows production-grade engineering practices:
- Full type hinting with mypy strict mode
- Comprehensive test suite with pytest
- Docker support for local development
- GitHub Actions CI pipeline
- Structured logging with correlation IDs
- Prometheus-compatible metrics
- Graceful shutdown handling
- Error recovery and retry mechanisms

## Project Structure

```
conductor/
├── __init__.py
├── cli.py
├── core/              # Core task queue functionality
├── db/                # Database operations and connection management
├── dlq/               # Dead letter queue implementation
├── observability/     # Logging, metrics, health checks
├── retry/             # Retry logic and policies
├── exceptions.py      # Custom exception hierarchy
├── utils.py           # Utility functions
├── models.py          # Data models and validation
└── examples/          # Real-world usage examples
```

## Target Audience

This project is designed to:
1. Solve a real engineering problem every backend team encounters
2. Demonstrate core strengths: async architecture, reliability patterns, production discipline  
3. Showcase technical leadership and engineering maturity
4. Serve as a portfolio project that attracts hiring attention

## Why This Project Works for Hiring

### Real Engineering Problem Solving
This project shows you can identify and solve actual engineering challenges that teams face daily.

### Production-Grade Skills
Demonstrates:
- Async programming with Python asyncio
- Database design and migration strategies
- Error handling and retry patterns
- Observability and monitoring
- System reliability and fault tolerance

### Community Engagement
The open-source nature shows you can create tools others want to use, which is valuable for engineering roles.

### Content Creation
Blog posts and documentation show communication skills that are essential in technical roles.

## Future Roadmap (Beyond Phase 1)

### Phase 2: Advanced Features (v0.2)
- Task routing & priority queues
- Scheduled & recurring tasks
- gRPC API support
- Web dashboard with metrics visualization

### Phase 3: Future Enhancements (v0.3+)
- Multi-database support (MySQL, SQLite)
- Distributed tracing (OpenTelemetry)
- Conductor Cloud SaaS offering
- Advanced workflow orchestration

## Contributing

Contributions are welcome! Please follow the existing code style and ensure all tests pass before submitting a pull request.

## License

MIT License - see LICENSE file for details.