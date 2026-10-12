# Image pinned by both interpreter patch version and immutable multi-architecture digest.
# Source: official python image index for python:3.12.12-slim-bookworm.
FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY configs/ ./configs/
COPY data/sample/ ./data/sample/
COPY src/ ./src/
COPY tests/ ./tests/
RUN python -m unittest discover -s tests -v
CMD ["python", "src/benchmark.py", "--config", "configs/config.json"]
