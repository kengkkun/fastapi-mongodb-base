FROM tiangolo/uvicorn-gunicorn:python3.11
WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/app/

COPY ./app /app/app

WORKDIR /app/app/


ENV PORT=8080
ENV HOST 0.0.0.0
ENV PORT 8080
ENV WORKERS_PER_CORE 1
ENV TIMEOUT 300
ENV GRACEFUL_TIMEOUT 300

CMD bash -c 'if [[ $INSTALL_DEV == "true" ]] ; then uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload ; else /start.sh ; fi'
