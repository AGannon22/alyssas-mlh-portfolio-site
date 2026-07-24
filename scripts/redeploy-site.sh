#!/bin/bash
set -e
cd ~
cd portfolio-website/alyssas-mlh-portfolio-site
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
