#!/usr/bin/env bash
set -euo pipefail

compose_cmd=(docker compose)

if ! "${compose_cmd[@]}" ps kafka >/dev/null 2>&1; then
  echo "Kafka service is not running. Start it with: ${compose_cmd[*]} up -d kafka" >&2
  exit 1
fi

create_topic() {
  local topic="$1"
  "${compose_cmd[@]}" exec -T kafka /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server kafka:9092 \
    --create \
    --if-not-exists \
    --topic "${topic}"
}

create_topic "miscrit-info"
create_topic "action"
