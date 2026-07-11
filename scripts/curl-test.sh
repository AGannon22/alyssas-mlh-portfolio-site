#!/usr/bin/env bash

set -a
source ../.env
set +a 

ENDPOINT="http://${URL}/api/timeline_post"

RAND=$RANDOM
NAME="Test User $RAND"
EMAIL="test$RAND@example.com"
CONTENT="Test post $RAND"

POST_BODY=$(curl -s -X POST "$ENDPOINT" \
  --data-urlencode "name=$NAME" \
  --data-urlencode "email=$EMAIL" \
  --data-urlencode "content=$CONTENT")

POST_ID=$(echo "$POST_BODY" | jq -r '.id')

GET_BODY=$(curl -s "$ENDPOINT")

MATCH=$(echo "$GET_BODY" | jq -r --arg id "$POST_ID" --arg name "$NAME" --arg email "$EMAIL" --arg content "$CONTENT" \
  '.timeline_posts[] | select(.id == ($id | tonumber) and .name == $name and .email == $email and .content == $content) | .id')

if [ "$MATCH" = "$POST_ID" ]; then
    echo "PASS"
else
    echo "FAIL"
fi