# =============================================================================
# Crypto Research Agent - Multi-stage Dockerfile
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /build
COPY pyproject.toml .
COPY README.md .
COPY src/ ./src/

# Install the package
RUN pip install --upgrade pip && \
    pip install .

# -----------------------------------------------------------------------------
# Stage 2: Runtime
# -----------------------------------------------------------------------------
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup prompts/ ./prompts/
COPY --chown=appuser:appgroup .claude/ ./.claude/

# Create output directory
RUN mkdir -p /app/output && chown appuser:appgroup /app/output

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.agent; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "src.agent"]

# -----------------------------------------------------------------------------
# Stage 3: Development (optional)
# -----------------------------------------------------------------------------
FROM runtime as development

# Switch back to root to install dev dependencies
USER root

# Copy dev requirements and install
COPY --from=builder /opt/venv /opt/venv
RUN pip install pytest pytest-asyncio ruff mypy

# Copy test files
COPY --chown=appuser:appgroup tests/ ./tests/

# Switch back to non-root user
USER appuser

# Override command for development
CMD ["pytest", "-v"]
