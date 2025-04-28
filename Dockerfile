FROM scratch as file
# Use a minimal base image
WORKDIR /app
ADD main.py pyproject.toml uv.lock README.md alembic.ini /app
ADD src /app/src
ADD migration /app/migration

# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS api

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --all-groups

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY --from=file /app /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -e .

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT ["python", "main.py"]

CMD []