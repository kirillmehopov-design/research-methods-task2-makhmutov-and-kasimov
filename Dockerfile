FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg
WORKDIR /app
COPY requirements.txt requirements.lock.txt ./
RUN python -m pip install --no-cache-dir -r requirements.lock.txt
COPY configs/ ./configs/
COPY data/ ./data/
COPY src/ ./src/
COPY tests/ ./tests/
COPY notebooks/ ./notebooks/
COPY docs/ ./docs/
COPY README.md ./README.md
ENV PYTHONPATH=/app
RUN python -m unittest discover -s tests -v
CMD ["python", "-m", "src.run_task3"]
