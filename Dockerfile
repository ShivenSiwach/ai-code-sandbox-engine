# We use docker:dind (Docker-in-Docker) as the base so the API can orchestrate other containers
FROM docker:24.0.5-dind

# Install Python and pip
RUN apk add --no-cache python3 py3-pip
WORKDIR /app

COPY requirements.txt .
# Create a virtual environment and install dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]