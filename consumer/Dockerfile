FROM python:3.11.9-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

COPY consumer/pyproject.toml ./
COPY consumer/uv.lock ./

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync --no-dev --no-group lint --no-cache

ENV PATH="/app/.venv/bin:$PATH"

CMD ["sh", "-c", "python -m consumer"]
