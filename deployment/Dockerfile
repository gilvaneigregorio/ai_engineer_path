# An example using multi-stage image builds to create a final image without uv.

# First, build the application in the `/app` directory.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Then, use a final image without uv
FROM python:3.12-slim-bookworm

# Install PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m app

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables for PostgreSQL
ENV PYTHONUNBUFFERED=1

EXPOSE 8501

USER app

CMD ["streamlit", "run", "src/main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]