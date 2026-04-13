# Stage 1: Build React frontend
FROM node:20-slim AS react-build

WORKDIR /app/frontend

# Copy package files first (better layer caching)
COPY package.json yarn.lock ./

# Install dependencies — use yarn since yarn.lock exists
RUN yarn install --frozen-lockfile --network-timeout 120000 || \
    yarn install --network-timeout 120000

# Copy source code
COPY . .

# Build React app
# CI=false prevents ESLint warnings from failing the build
# REACT_APP_BACKEND_URL="" means API calls use relative paths (nginx proxies /api/)
ENV CI=false
ENV REACT_APP_BACKEND_URL=""
ENV GENERATE_SOURCEMAP=false
RUN yarn build

# Stage 2: Django serves the built React app
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy React build output into Django static serving path
COPY --from=react-build /app/frontend/build /app/build

RUN python manage.py collectstatic --noinput || true

EXPOSE 8001
