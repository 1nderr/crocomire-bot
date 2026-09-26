FROM python:3.8
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_NO_DEV=1

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --locked

COPY . /app

CMD [ "uv", "run", "crocbot.py" ]
