FROM python:3.12-slim

# Security: Create a non-root user to run the app
RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

# 1. Critical Update: Upgrade system packages to fix vulnerabilities like CVE-2026-0861
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 2. Path Correction: Copy requirements from the restaurant subdirectory
COPY restaurant/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Add this line to collect static files
RUN python manage.py collectstatic --noinput

# Ensure the non-root user has access to the new folder
RUN chown -R django:django /app/staticfiles

USER django

# Security & Performance: Set Production Environment Variables
ENV DEBUG=False
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health Check: Verifies the service is responding on the expected port
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

EXPOSE 8000

# Use Gunicorn as the production-grade WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "restaurant.wsgi:application"]
