# P1: Carbon–Silion universe service (Flask) + data volume
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CS_UNIVERSE_HOST=0.0.0.0 \
    CS_UNIVERSE_PORT=8765
COPY python/requirements-carbon-silicon.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY python /app/python
# Import path: /app/python is the parent of package
ENV PYTHONPATH=/app/python
EXPOSE 8765
# Create writable data dir
RUN mkdir -p /app/python/data
CMD ["python", "-m", "carbon_silicon_universe"]
