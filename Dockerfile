<<<<<<< HEAD
# Multi-stage build for FinAgent Meta-Supervisor
# Stage 1: Build environment
FROM python:3.10-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment variables
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files
WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev --no-cache

# Stage 2: Production runtime
FROM python:3.10-slim as runtime

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy uv from builder stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy virtual environment from builder stage
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Make sure to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser .env.template ./.env

# Copy startup script
COPY --chown=appuser:appuser run.sh ./
RUN chmod +x run.sh

# Create necessary directories
RUN mkdir -p /app/logs && chown appuser:appuser /app/logs

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Add metadata labels
LABEL maintainer="FinAgent-Lab <finlabe@finlab.com>"
LABEL version="1.0.0"
LABEL description="Meta-Supervisor for Financial Agent System"

# Expose port
EXPOSE 8000

# Set default environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["./run.sh"]
=======
# Python 3.10 베이스 이미지 사용 (pyproject.toml과 일치)
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# uv 설치
RUN pip install uv

# 프로젝트 파일 복사
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# 의존성 설치
RUN uv sync --frozen

# 포트 설정
EXPOSE 8000

# Health check 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 실행 명령
CMD ["uv", "run", "uvicorn", "src.meta_supervisor.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 533bdfc41fe5343f9e89a6c207c3559c3fafb65d
