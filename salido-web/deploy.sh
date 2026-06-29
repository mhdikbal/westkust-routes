#!/bin/bash
# deploy.sh — build Astro dan upload ke server
set -e

SERVER="westkust-prod"
REMOTE_DIR="/var/www/salido/dist"

echo ">>> [1/3] Build Astro..."
source ~/.nvm/nvm.sh && nvm use 22
npm run build

echo ">>> [2/3] Upload ke server..."
rsync -avz --delete \
  -e "ssh" \
  dist/ \
  ubuntu@${SERVER}:${REMOTE_DIR}/

echo ">>> [3/3] Reload Nginx..."
ssh ${SERVER} "sudo nginx -t && sudo systemctl reload nginx"

echo ">>> Deploy selesai! https://salido.my.id"
