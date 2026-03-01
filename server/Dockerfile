FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY server/pyproject.toml .
RUN uv pip install --system .
COPY server/ .
COPY tutorial/ /app/tutorial/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
