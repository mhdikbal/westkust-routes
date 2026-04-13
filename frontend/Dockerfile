# Stage 1: Build React frontend
FROM node:20-slim AS react-build

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY package.json yarn.lock* ./
RUN npm install --legacy-peer-deps 2>/dev/null || yarn install --frozen-lockfile 2>/dev/null || npm install

# Copy source and build
COPY . .
ENV REACT_APP_BACKEND_URL=""
RUN npm run build || yarn build

# Stage 2: Django serves the built React app
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy React build output into Django static
COPY --from=react-build /app/frontend/build /app/build

RUN python manage.py collectstatic --noinput || true

EXPOSE 8001
